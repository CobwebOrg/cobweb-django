from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views import generic
from django.apps import apps
from django.urls import reverse

from . import models

class ProjectIndexView(generic.ListView):
    model = models.Project

class ProjectDetailView(generic.DetailView):
    model = models.Project

def object_list(request, model_name):
    try:
        model = apps.get_model('registry', model_name)
        return generic.ListView.as_view(model=model, template_name='project_list.html')(request)
    except:
        raise Http404("{model_name}: That's not a thing we have.".format(model_name=model_name))

def object_view(request, model_name, pk):
    try:
        model = apps.get_model('registry', model_name)
    except:
        raise Http404("{model_name}: no such class.".format(model_name=model_name))
    
    fields = [field.name for field in model._meta.fields[1:] if field.editable]
    if pk == "new":
        return generic.CreateView.as_view(
            model=model, 
            template_name='registry/object_form.html',
            fields=fields,
            success_url=reverse('registry:object_list', kwargs={'model_name': model_name}),
        )(request)
    else:
        try:
            current_object = get_object_or_404(model, pk=pk)
            return generic.UpdateView.as_view(
                model=model,
                template_name='registry/object_detail.html',
                fields=fields,
                success_url=reverse('registry:object_list', kwargs={'model_name': model_name}),
            )(request, pk=pk)
        except:
            raise Http404("Can't find {model_name} {pk}.".format(model_name=model_name, pk=pk))

# def save_object(request, model_name, pk):
#     try:
#         model = apps.get_model('registry', model_name)
#         if pk == 'new':
#             current_object = model()