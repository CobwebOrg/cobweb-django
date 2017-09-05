from django.apps import apps
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from . import forms, models


#
#   Inline Views
#
        

        


#
#   Page Views
#

class UserIndexView(generic.ListView):
    model = auth.models.User
    template_name = "user_list.html"

class UserDetailView(generic.DetailView):
    model = auth.models.User
    template_name = "user_detail.html"

class AgentDetailView(generic.DetailView):
    model = models.Agent
    template_name = "user_detail.html"

class UserCreateView(generic.CreateView):
    model = auth.models.User
    template_name = "generic_form.html"
    form_class = forms.UserForm

class ProjectIndexView(generic.ListView):
    model = models.Project
    template_name = "project_list.html"

class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = "project_detail.html"

class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.established_by = self.request.user.agent
        candidate.save()
        return super().form_valid(form)

class NominationDetailView(generic.DetailView):
    model = models.Nomination
    template_name = 'nomination_detail.html'

class NominationCreateView(generic.CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominationForm

    def form_valid(self, form):
        print(self.request.path)
        print(self.kwargs)
        candidate = form.save(commit=False)
        candidate.project = models.Project.objects.get(pk=self.kwargs['project_id'])
        self.success_url = candidate.project.get_absolute_url()
        candidate.nominated_by = self.request.user.agent
        candidate.save()
        return super().form_valid(form)

def object_list_view(request, model_name):
    model = apps.get_model('cobweb', model_name)
    request.model_name = model_name
    request.verbose_name_plural = model._meta.verbose_name_plural
    return generic.ListView.as_view(model=model, template_name='object_list.html')(request)


