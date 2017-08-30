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
        # user = auth.models.User.objects.get(user=self.request.user)
        # candidate.established_by = models.Agent.objects.get(user=self.request.user)
        candidate.established_by = user=self.request.user.agent
        candidate.save()
        return super().form_valid(form)

def object_list_view(request, model_name):
    model = apps.get_model('cobweb', model_name)
    request.model_name = model_name
    request.verbose_name_plural = model._meta.verbose_name_plural
    return generic.ListView.as_view(model=model, template_name='object_list.html')(request)

def object_view(request, model_name, pk):
    try:
        model = apps.get_model('cobweb', model_name)
    except:
        raise Http404("{model_name}: no such model.".format(model_name=model_name))
    
    as_view_arguments = dict(
        model=model, 
        template_name='object_form.html',
        fields=[field.name for field in model._meta.fields[1:] if field.editable],
        success_url=reverse('object_list', kwargs={'model_name': model_name}),   
    )
    view_function_arguments = dict()
    if pk == "new":
        generic_view_object = generic.CreateView
    else:
        generic_view_object = generic.UpdateView
        view_function_arguments['pk'] = pk
        
    return generic_view_object.as_view(**as_view_arguments)(request, **view_function_arguments)
        # except:
            # raise Http404("Can't find {model_name} {pk}.".format(model_name=model_name, pk=pk))

