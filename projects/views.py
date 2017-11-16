from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from reversion.views import RevisionMixin

from webresources.models import Resource

from projects import models, forms


class ProjectIndexView(ListView):
    model = models.Project
    template_name = "project_list.html"


class ProjectDetailView(DetailView):
    model = models.Project
    template_name = "project.html"


class ProjectCreateView(LoginRequiredMixin, RevisionMixin, CreateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm

    # def form_valid(self, form):
    #     candidate = form.save(commit=False)
    #     candidate.administered_by.add(self.request.user)

    #     candidate.save()
    #     return super().form_valid(form)


class ProjectUpdateView(UserPassesTestMixin, RevisionMixin, UpdateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm

    def test_func(self):
        return self.get_object().is_admin(self.request.user)


class NominationDetailView(DetailView):
    model = models.Nomination
    template_name = 'nomination_detail.html'


class NominationCreateView(UserPassesTestMixin, RevisionMixin, CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominateToProjectForm

    def form_valid(self, form):
        print(self.request.path)
        print(self.kwargs)
        candidate = form.save(commit=False)
        candidate.project = self.get_project()
        self.success_url = candidate.project.get_absolute_url()
        candidate.nominated_by = self.request.user
        candidate.save()
        return super().form_valid(form)

    def get_initial(self):
        return {
            'nominated_by': self.request.user,
            'project': self.get_project(),
        }

    def get_project(self):
        return models.Project.objects.get(pk=self.kwargs['project_id'])

    def test_func(self):
        return self.get_project().is_nominator(self.request.user)


class ResourceNominateView(RevisionMixin, CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.ResourceNominateForm

    def form_valid(self, form):
        print(self.request.path)
        print(self.kwargs)
        candidate = form.save(commit=False)
        candidate.resource = self.get_resource()
        self.success_url = candidate.resource.get_absolute_url()
        candidate.nominated_by = self.request.user
        candidate.save()
        return super().form_valid(form)

    def get_initial(self):
        return {
            'nominated_by': self.request.user,
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
