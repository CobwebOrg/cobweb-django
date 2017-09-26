from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from projects import models, forms



class ProjectIndexView(ListView):
    model = models.Project
    template_name = "project_list.html"

class ProjectDetailView(DetailView):
    model = models.Project
    template_name = "project_detail.html"

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.administered_by.add(models.Agent.objects.get(
            user=self.request.user,
            software=models.Software.current_website_software(),
        ))

        candidate.save()
        return super().form_valid(form)

class NominationDetailView(DetailView):
    model = models.Nomination
    template_name = 'nomination_detail.html'

class NominationCreateView(CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominationForm

    def form_valid(self, form):
        print(self.request.path)
        print(self.kwargs)
        candidate = form.save(commit=False)
        candidate.project = models.Project.objects.get(pk=self.kwargs['project_id'])
        self.success_url = candidate.project.get_absolute_url()
        candidate.nominated_by = models.Agent.objects.get(
            user=self.request.user,
            software=models.Software.current_website_software(),
        )
        candidate.save()
        return super().form_valid(form)