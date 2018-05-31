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


class ProjectDetailView(django_tables2.SingleTableMixin, DetailView):
    model = models.Project
    template_name = "projects/project.html"
    table_class = NominationTable
    section = 'project'

    def get_table_data(self):
        return self.object.nominations.all()


class ProjectCreateView(LoginRequiredMixin, RevisionMixin, CreateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm
    section = 'project'

    def get_initial(self):
        initial = super().get_initial()
        initial['administrators'] = {self.request.user.pk}
        print(initial)
        return initial

    # def form_valid(self, form):
    #     candidate = form.save(commit=False)
    #     candidate.administrators.add(self.request.user)

    #     candidate.save()
    #     return super().form_valid(form)


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
                'admin_version': self.get_object().is_admin(self.request.user)
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

class NominationView(RevisionMixin, InlineFormSetView, UpdateView):
    model = models.Nomination
    inline_model = models.Claim
    template_name = 'projects/nomination.html'
    form_class = forms.NominationForm
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def get_factory_kwargs(self):
        kwargs = super().get_factory_kwargs()
        kwargs['extra'] = 1
        kwargs['form'] = forms.ClaimForm
        return kwargs


class NominationCreateView(UserPassesTestMixin, RevisionMixin, CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominationForm
    section = 'nomination'

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.project = self.get_project()
        self.success_url = candidate.project.get_absolute_url()
        candidate.save()
        return super().form_valid(form)

    def get_initial(self):
        return {
            'endorsements': [self.request.user],
            'project': self.get_project(),
        }

    def get_project(self):
        return models.Project.objects.get(pk=self.kwargs['project_id'])

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


# class NominationUpdateView(UserPassesTestMixin, RevisionMixin, UpdateView):
#     model = models.Nomination
#     template_name = 'generic_form.html'
#     form_class = forms.NominationForm
#     section = 'nomination'

#     def test_func(self):
#         return self.get_object().project.is_nominator(self.request.user)

class NominationClaimsView(RevisionMixin, InlineFormSetView, UpdateView):
    model = models.Nomination
    inline_model = models.Claim
    template_name = 'projects/nomination.html'
    form_class = forms.NominationForm
    slug_url_kwarg = 'url'
    
    def get_factory_kwargs(self):
        kwargs = super().get_factory_kwargs()
        kwargs['extra'] = 1
        kwargs['form'] = forms.ClaimForm
        return kwargs
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.filter(project_id=self.kwargs['project_id']).get(resource__url=self.kwargs['url'])


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
