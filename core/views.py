from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic
from reversion.views import RevisionMixin

from core.forms import UserForm
    

class UserIndexView(generic.ListView):
    model = get_user_model()
    template_name = "user_list.html"

class UserDetailView(generic.DetailView):
    model = get_user_model()
    template_name = "user_detail.html"

class UserCreateView(RevisionMixin, generic.CreateView):
    model = get_user_model()
    template_name = "generic_form.html"
    form_class = UserForm

class UserUpdateView(RevisionMixin, generic.UpdateView):
    model = get_user_model()
    template_name = "generic_form.html"
    form_class = UserForm
