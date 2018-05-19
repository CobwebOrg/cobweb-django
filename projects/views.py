import django_tables2
import haystack
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView
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


class ProjectDetailView(django_tables2.SingleTableMixin, DetailView):
    model = models.Project
    template_name = "project.html"
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


class ProjectUpdateView(UserPassesTestMixin, RevisionMixin, UpdateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm
    section = 'project'

    def test_func(self):
        return self.get_object().is_admin(self.request.user)


class NominationDetailView(django_tables2.SingleTableMixin, DetailView):
    model = models.Nomination
    template_name = 'nomination.html'
    section = 'nomination'
    table_class = ClaimTable

    def get_table_data(self):
        return self.object.claims.all()


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


class NominationUpdateView(UserPassesTestMixin, RevisionMixin, UpdateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominationForm
    section = 'nomination'

    def test_func(self):
        return self.get_object().project.is_nominator(self.request.user)


class ClaimDetailView(DetailView):
    model = models.Claim
    template_name = 'projects/claim.html'
    section = 'claim'


class ClaimFormViewMixin(UserPassesTestMixin, RevisionMixin):
    model = models.Claim
    template_name = 'generic_form.html'
    form_class = forms.ClaimForm
    section = 'claim'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['collection'].queryset = (
            self.request.user.collections_administered
        )
        return form

    def test_func(self):
        return self.request.user.collections_administered.count() > 0


class ClaimCreateView(ClaimFormViewMixin, CreateView):

    def get_initial(self):
        return {'nomination': self.kwargs['nomination_pk']}


class ClaimUpdateView(ClaimFormViewMixin, UpdateView):
    pass
