from typing import Optional

import django_tables2
import haystack
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from extra_views import InlineFormSetView
from reversion.views import RevisionMixin

from api.serializers import ResourceSerializer
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
                'new_item_link': reverse_lazy('project_create'),
            })
        return context_data
    
    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({'new_item_link': reverse_lazy('project_create')})
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
        kwargs.update({
            'editable': True,
            'request': self.request,
        })
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

    def get_context_data(self, **kwargs):
        if 'select_tab' not in kwargs:
            kwargs['show_noms'] = True if len(self.request.GET) > 0 else False

        if self.object.is_admin(self.request.user):
            kwargs.update({
                'delete_url': reverse_lazy('project_delete', kwargs=self.kwargs),
                'delete_text': format_html("""
                    <p>Are you sure you want to delete the project "{project}"?</p>
                    <p>All associated nominations and claims will be deleted.</p>
                """, project=self.object),
            })

        return super().get_context_data(**kwargs)
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({
                'editable': self.get_object().is_admin(self.request.user),
            })
        kwargs.update({
            'request': self.request,
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

        kwargs.update({'exclude': ['project']})

        return kwargs


class ProjectDeleteView(UserPassesTestMixin, FormMessageMixin, DeleteView):
    model = models.Project
    success_url = reverse_lazy('project_list')
    template_name = 'delete_confirm.html'
    slug_field = 'slug'

    def test_func(self):
        return self.get_object().is_admin(self.request.user)


class NominationUpdateView(FormMessageMixin, RevisionMixin,
                           django_tables2.SingleTableMixin, UpdateView):
    model = models.Nomination
    form_class = forms.NominationForm
    template_name = 'generic_form.html'
    table_class = ClaimTable

    def get_context_data(self, **kwargs):
        if self.object.project.is_admin(self.request.user):
            kwargs.update({
                'delete_url': reverse_lazy('nomination_delete', kwargs=self.kwargs),
                'delete_text': format_html("""
                    <p>Are you sure you want to delete the nomination of "{url}"
                       to the project "{project}"?</p>
                    <p>All associated claims will be deleted.</p>
                """, project=self.object.project, url=self.object.resource.url),
            })
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()

        kwargs.update({
            'editable': self.get_object().is_admin(self.request.user),
            'tabbed': False,
            'request': self.request,
        })

        if 'data' in kwargs:
            assert kwargs['data']['resource'] == self.kwargs['url']
            kwargs['data'] = kwargs['data'].copy()
            kwargs['data'].update({
                'project': self.kwargs['project_pk'],
                'nominated_by': self.request.user.id,  # works bc MultiValueDict magic...
            })
        kwargs['table'] = self.get_table()

        # If there's metadata about the resource, data for the react component
        if self.object.resource.has_metadata:
            kwargs['react_data'] = {
                'user': self.request.user.username,
                'hide_sidebar': True,
                'resource': ResourceSerializer(self.object.resource).data,
            }

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

    def get_success_message(self, cleaned_data):
        return f'Successfully saved changes to nomination of {self.object.resource}'
    
    def get_table_data(self):
        return self.get_object().claims.all()
        # return (haystack.query.SearchQuerySet()
        #         .filter(django_ct__exact='projects.claim')
        #         .filter(nomination_pk__exact=self.get_object().pk))

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        if self.object.can_claim(self.request.user):
            kwargs['new_item_link'] = self.get_object().get_claim_url()
        kwargs.update({
            'exclude': ['nomination'],
        })
        return kwargs

    def get_project(self):
        if not (hasattr(self, '_project') and isinstance(self._project, models.Project)):
          self._project = models.Project.objects.get(pk=self.kwargs['project_pk'])
        return self._project
    

class NominationCreateView(FormMessageMixin, UserPassesTestMixin,
                           RevisionMixin, CreateView):
    model = models.Nomination
    # template_name = 'projects/nomination_create.html'
    template_name = 'generic_form.html'
    form_class = forms.NominationForm
    _project = None

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
            'request': self.request,
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

    def get_success_message(self, cleaned_data):
        return f'Successfully nominated {self.object.resource}'

    def test_func(self):
        return self.get_project().is_nominator(self.request.user)


class NominationDeleteView(UserPassesTestMixin, FormMessageMixin, DeleteView):
    model = models.Nomination
    template_name = 'delete_confirm.html'

    def get_object(self, queryset=None):
        try:
            obj = models.Nomination.objects.get(
                project__pk=self.kwargs['project_pk'],
                resource__url=self.kwargs['url'],
            )
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj
    
    def get_success_url(self):
        return self.object.project.get_absolute_url()

    def test_func(self):
        return self.get_object().project.is_admin(self.request.user)


class ClaimFormMixin(FormMessageMixin, RevisionMixin):
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

    def get_success_url(self) -> str:
        return self.object.nomination.get_absolute_url()


class ClaimCreateView(UserPassesTestMixin, ClaimFormMixin, CreateView):
    success_message = "Nomination successfully claimed"

    def test_func(self):
        return self.get_nomination().can_claim(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        nomination = self.get_nomination()
        kwargs.update({
            'editable': True,
            'request': self.request,
            'instance': models.Claim(
                nomination=nomination,
                organization=self.request.user.organization,
                crawl_start_date=nomination.crawl_start_date,
                crawl_end_date=nomination.crawl_end_date,
                crawl_frequency=nomination.crawl_frequency,
                follow_links=nomination.follow_links,
                page_scope=nomination.page_scope,
                ignore_robots_txt=nomination.ignore_robots_txt,
                rights_considerations=nomination.rights_considerations,
            ),
        })
        return kwargs

    def get_nomination(self):
        """Get the nomination being claimed."""

        if self._nomination is None:
            self._nomination = models.Nomination.objects.get(pk=self.kwargs['nomination_pk'])
        return self._nomination

    def get_success_message(self, cleaned_data):
        return f'Successfully claimed {self.object.nomination.resource}'


class ClaimUpdateView(ClaimFormMixin, UpdateView):

    def get_context_data(self, **kwargs) -> dict:
        if (self.object.nomination.project.is_admin(self.request.user)
            or self.object.organization.is_admin(self.request.user)):
            context = {
                'delete_url': reverse_lazy('claim_delete', kwargs=self.kwargs),
            }
        else:
            context = {}
        context.update(kwargs)
        return super().get_context_data(**context)  # type: ignore

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs.update({
            'editable': self.object.is_admin(self.request.user),
            'request': self.request,
        })
        return kwargs

    def get_nomination(self):
        """Get the nomination being claimed."""

        return self.get_object().nomination

    def get_success_message(self, cleaned_data):
        return f'Successfully updated claim of {self.object.nomination.resource}'


class ClaimDeleteView(UserPassesTestMixin, FormMessageMixin, DeleteView):
    model = models.Claim
    template_name = 'delete_confirm.html'

    def get_success_url(self):
        return self.object.nomination.get_absolute_url()

    def test_func(self):
        obj = self.get_object()
        return (obj.nomination.project.is_admin(self.request.user)
                or obj.organization.is_admin(self.request.user))
