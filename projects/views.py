from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from reversion.views import RevisionMixin

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
    # formset_class = forms.ProjectMDInlineFormset

    def test_func(self):
        return self.get_object().can_administer(self.request.user)

class NominationDetailView(DetailView):
    model = models.Nomination
    template_name = 'nomination_detail.html'

class NominationCreateView(UserPassesTestMixin, RevisionMixin, CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominationForm

    def form_valid(self, form):
        print(self.request.path)
        print(self.kwargs)
        candidate = form.save(commit=False)
        candidate.project = self.get_project()
        self.success_url = candidate.project.get_absolute_url()
        candidate.nominated_by = self.request.user
        candidate.save()
        return super().form_valid(form)

    def get_project(self):
        return models.Project.objects.get(pk=self.kwargs['project_id'])

    def test_func(self):
        return self.get_project().can_nominate(self.request.user)