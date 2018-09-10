from typing import Optional

import django_tables2
import haystack
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from extra_views import InlineFormSetView
from reversion.views import RevisionMixin

from core.models import Resource
from core.views import CobwebBaseIndexView, FormMessageMixin
from projects import forms, models
from projects.tables import ClaimTable, NominationTable, ProjectTable


class ProjectIndexView(CobwebBaseIndexView):
    model = models.Project
    table_class = ProjectTable
    django_ct = 'projects.project'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context_data.update({
                'new_item_link': reverse('project_create'),
            })
        return context_data
    
    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({'new_item_link': reverse('project_create')})
        return kwargs


class ProjectCreateView(LoginRequiredMixin, FormMessageMixin, RevisionMixin,
                        django_tables2.SingleTableMixin, CreateView):
    model = models.Project
    template_name = 'projects/project.html'
    form_class = forms.ProjectForm
    table_class = NominationTable

    def get_initial(self):
        initial = super().get_initial()
        initial['administrators'] = {self.request.user.pk}
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['editable'] = True
        return kwargs

    def get_table_data(self):
        return haystack.query.SearchQuerySet().none()

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        kwargs['exclude'] = ('claim_link',)
        return kwargs


class ProjectView(FormMessageMixin, RevisionMixin, django_tables2.SingleTableMixin,
                  UpdateView):
    model = models.Project
    template_name = 'projects/project.html'
    form_class = forms.ProjectForm
    table_class = NominationTable
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({
                'editable': self.get_object().is_admin(self.request.user)
            })
        return kwargs

    def get_table_data(self):
        return (haystack.query.SearchQuerySet()
                .filter(django_ct__exact='projects.nomination')
                .filter(project_pk__exact=self.get_object().pk))

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        proj = self.get_object()

        if proj.is_nominator(self.request.user):
            kwargs.update({'new_item_link': proj.get_add_nomination_url()})

        if not (self.request.user.is_authenticated and self.request.user.can_claim()):
            kwargs.update({'exclude': ('claim_link',)})
        
        return kwargs


class NominationUpdateView(RevisionMixin, django_tables2.SingleTableMixin,
                           UpdateView):
    model = models.Nomination
    form_class = forms.NominationForm
    template_name = 'projects/nomination.html'
    table_class = ClaimTable

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'editable': self.get_object().is_admin(self.request.user),
            'tabbed': True,
        })
        if 'data' in kwargs:
            assert kwargs['data']['resource'] == self.kwargs['url']
            kwargs['data'] = kwargs['data'].copy()
            kwargs['data'].update({
                'project': self.kwargs['project_pk'],
                'nominated_by': self.request.user.id,  # works bc MultiValueDict magic...
            })
        return kwargs

    def get_object(self, queryset=None):
        try:
            # Get the single item from the filtered queryset
            obj =  models.Nomination.objects.get(
                project__pk=self.kwargs['project_pk'],
                resource__url=self.kwargs['url'],
            )
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': queryset.model._meta.verbose_name})
        return obj
    
    def get_table_data(self):
        return self.get_object().claims.all()
        # return (haystack.query.SearchQuerySet()
        #         .filter(django_ct__exact='projects.claim')
        #         .filter(nomination_pk__exact=self.get_object().pk))

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        if self.request.user.is_authenticated and self.request.user.can_claim():
            kwargs['new_item_link'] = self.get_object().get_claim_url()
        kwargs.update({'exclude': ('nomination',)})
        return kwargs
    

class NominationCreateView(UserPassesTestMixin, RevisionMixin, CreateView):
    model = models.Nomination
    # template_name = 'projects/nomination_create.html'
    template_name = 'generic_form.html'
    form_class = forms.NominationForm
    _project = None

    # def form_valid(self, form):
    #     candidate = form.save(commit=False)
    #     candidate.project = self.get_project()
    #     self.success_url = candidate.project.get_absolute_url()
    #     candidate.save()
    #     return super().form_valid(form)

    def get_initial(self):
        return {
            'nominated_by': (self.request.user,),
            'project': self.get_project().pk,
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project': self.get_project(),
        })
        return context
    
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'editable': True,
            'tabbed': False,
        })
        if 'data' in form_kwargs:
            form_kwargs['data'] = form_kwargs['data'].copy()
            form_kwargs['data'].update({
                'project': self.kwargs['project_pk'],
                'nominated_by': self.request.user.id,  # works bc MultiValueDict magic...
            })
        return form_kwargs


    def get_project(self):
        if not (hasattr(self, '_project') and isinstance(self._project, models.Project)):
          self._project = models.Project.objects.get(pk=self.kwargs['project_pk'])
        return self._project

    def test_func(self):
        return self.get_project().is_nominator(self.request.user)


class ClaimFormMixin:
    model = models.Claim
    template_name = 'projects/claim.html'
    form_class = forms.ClaimForm
    _nomination: Optional[models.Nomination] = None

    def get_context_data(self, **kwargs) -> dict:
        """Insert forms w/ the parent nomination & project into the context dict."""

        nomination = self.get_nomination()
        context = {
            'nomination_form': forms.NominationForm(instance=nomination, tabbed=True),
            'project_form': forms.ProjectForm(instance=nomination.project)
        }
        context.update(kwargs)
        return super().get_context_data(**context)  # type: ignore


class ClaimCreateView(UserPassesTestMixin, RevisionMixin, ClaimFormMixin, CreateView):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.can_claim()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        nomination = self.get_nomination()
        kwargs.update({
            'editable': True,
            'instance': models.Claim(
                nomination=nomination,
                organization=self.request.user.organization,
                crawl_start_date = nomination.crawl_start_date,
                crawl_end_date = nomination.crawl_end_date,
                crawl_frequency = nomination.crawl_frequency,
                follow_links = nomination.follow_links,
                page_scope = nomination.page_scope,
            ),
        })
        return kwargs

    def get_nomination(self):
        """Get the nomination being claimed."""

        if self._nomination is None:
            self._nomination = models.Nomination.objects.get(pk=self.kwargs['nomination_pk'])
        return self._nomination


class ClaimUpdateView(RevisionMixin, ClaimFormMixin, UpdateView):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        nomination = self.get_nomination()
        kwargs.update({
            'editable': self.object.is_admin(self.request.user),
            'instance': models.Claim(
                nomination=nomination,
                organization=self.request.user.organization,
                crawl_start_date = nomination.crawl_start_date,
                crawl_end_date = nomination.crawl_end_date,
                crawl_frequency = nomination.crawl_frequency,
                follow_links = nomination.follow_links,
                page_scope = nomination.page_scope,
            ),
        })
        return kwargs

    def get_nomination(self):
        """Get the nomination being claimed."""

        return self.get_object().nomination


def claim_view(request, **kwargs):
    pass
