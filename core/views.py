from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from core.forms import UserForm

class UserIndexView(generic.ListView):
    model = get_user_model()
    template_name = "user_list.html"

class UserDetailView(generic.DetailView):
    model = get_user_model()
    template_name = "user_detail.html"

class UserCreateView(generic.CreateView):
    model = get_user_model()
    template_name = "generic_form.html"
    form_class = UserForm

class UserUpdateView(generic.UpdateView):
    model = get_user_model()
    template_name = "generic_form.html"
    form_class = UserForm

def object_list_view(request, model_name):
    model = apps.get_model('cobweb', model_name)
    request.model_name = model_name
    request.verbose_name_plural = model._meta.verbose_name_plural
    return generic.ListView.as_view(model=model, template_name='object_list.html')(request)


