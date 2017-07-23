from django.shortcuts import render
from django.views import generic
from django.apps import apps

from . import models

class ProjectIndexView(generic.ListView):
    model = models.Project

class ProjectDetailView(generic.DetailView):
    model = models.Project

# class ObjectView(generic.UpdateView):
#     print(locals())
#     model = apps.get_model('registry', model_name)
#     fields = [field.name for field in fields[1:] if not field.editable]
#
#     def as_view()