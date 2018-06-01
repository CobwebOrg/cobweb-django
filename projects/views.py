import django_tables2
import haystack
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView
from extra_views import InlineFormSetView
from reversion.views import RevisionMixin

from core.models import Resource
from core.views import CobwebBaseIndexView

from projects import models, forms
from projects.tables import ProjectTable, NominationTable, ClaimTable


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


class ProjectCreateView(LoginRequiredMixin, RevisionMixin, CreateView):
    model = models.Project
    template_name = 'projects/project_create.html'
    form_class = forms.ProjectForm

    def get_initial(self):
        initial = super().get_initial()
        initial['administrators'] = {self.request.user.pk}
        print(initial)
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['editable'] = True
        return kwargs


class ProjectSummaryView(RevisionMixin, UpdateView):
    model = models.Project
    template_name = 'projects/project.html'
    form_class = forms.ProjectForm
    
    @property
    def summary(self):
        return type(self) is ProjectSummaryView

    @property
    def nominations(self):
        return type(self) is ProjectNominationsView

    @property
    def notes(self):
        return False  # type(self) is ProjectNotesView

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if self.summary and hasattr(self, 'object'):
            kwargs.update({
                'editable': self.get_object().is_admin(self.request.user)
            })
        return kwargs


class ProjectNominationsView(django_tables2.SingleTableMixin, ProjectSummaryView):
    table_class = NominationTable
    right_panel = 'nominations'

    def get_table_data(self):
        return (haystack.query.SearchQuerySet()
                .filter(django_ct__exact='projects.nomination')
                .filter(project_pk__exact=self.get_object().pk))

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        proj = self.get_object()

        if proj.is_nominator(self.request.user):
            kwargs.update({'new_item_link': proj.get_add_nomination_url()})

        if not self.request.user.can_claim():
            kwargs.update({'exclude': ('claim_link',)})
        
        return kwargs


class NominationUpdateView(RevisionMixin, UpdateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominationForm
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        project = self.get_object().project
        kwargs['editable'] = project.is_nominator(self.request.user)
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
            'project': self.get_project(),
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proj = self.get_project()
        context.update({
            'project': proj,
            # 'project_form': forms.ProjectForm(instance=proj),
        })
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['editable'] = True
        return kwargs

    def get_project(self):
        if not (hasattr(self, '_project') and isinstance(self._project, models.Project)):
          self._project = models.Project.objects.get(pk=self.kwargs['project_id'])
        return self._project

    def test_func(self):
        return self.get_project().is_nominator(self.request.user)


class ResourceNominateView(RevisionMixin, CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominationForm
    section = 'nomination'

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.resource = self.get_resource()
        return super().form_valid(form)

    def get_initial(self):
        return {
            'endorsements': [self.request.user],
            'resource': self.kwargs['url'],
        }

    def get_resource(self):
        try:
            obj = Resource.objects.get(url=self.kwargs['url'])
        except Resource.DoesNotExist:
            obj = Resource(url=self.kwargs['url'])
        except Exception as ex:
            raise ex

        return obj

    def test_func(self):
        return True
        # return self.get_project().is_nominator(self.request.user)

class NominationClaimsView(RevisionMixin, InlineFormSetView, UpdateView):
    model = models.Nomination
    inline_model = models.Claim
    form_class = forms.NominationDisplayForm
    template_name = 'projects/nomination.html'

    def get_object(self, queryset=None):
        assert queryset is None, "NominationClaimsView doesn't take a queryset."
        try:
            # Get the single item from the filtered queryset
            obj =  models.Nomination.objects.filter(
                project__pk=self.kwargs['project_pk'],
                resource__url=self.kwargs['url'],
            ).get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': queryset.model._meta.verbose_name})
        return obj
        
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        project = self.get_object().project
        kwargs['editable'] = False
        return kwargs
    
    def get_factory_kwargs(self):
        kwargs = super().get_factory_kwargs()
        kwargs['extra'] = 1
        kwargs['form'] = forms.ClaimForm
        return kwargs


class ClaimDetailView(DetailView):
    model = models.Claim
    template_name = 'projects/claim.html'


class ClaimFormViewMixin(UserPassesTestMixin, RevisionMixin):
    model = models.Claim
    template_name = 'generic_form.html'
    form_class = forms.ClaimForm

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['organization'].queryset = (
            self.request.user.collections_administered
        )
        return form

    def test_func(self):
        return self.request.user.can_claim()


class ClaimCreateView(ClaimFormViewMixin, CreateView):

    def get_initial(self):
        return {'nomination': self.kwargs['nomination_pk']}


class ClaimUpdateView(ClaimFormViewMixin, UpdateView):
    pass
