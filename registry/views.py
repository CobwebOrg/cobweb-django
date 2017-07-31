from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views import generic
from django.apps import apps
from django.urls import reverse
from django.template.loader import render_to_string

from . import models, tables


#
#   Inline Views
#
        

        
table_class_key = {
    models.Institution: tables.InstitutionTable,
    models.Agent: tables.AgentTable,
    models.Project: tables.ProjectTable,
    models.Seed: tables.SeedTable,
    models.Claim: tables.ClaimTable,
    models.Holding: tables.HoldingTable,
}

#
#   Page Views
#

class ProjectIndexView(generic.ListView):
    model = models.Project

class ProjectDetailView(generic.DetailView):
    model = models.Project

def object_list_view(request, model_name):
    model = apps.get_model('registry', model_name)
    request.model_name = model_name
    request.verbose_name_plural = model._meta.verbose_name_plural
    request.table = table_class_key[model](model.objects.all())
    return generic.ListView.as_view(model=model, template_name='registry/object_list.html')(request)

def object_view(request, model_name, pk):
    try:
        model = apps.get_model('registry', model_name)
    except:
        raise Http404("{model_name}: no such model.".format(model_name=model_name))
    
    as_view_arguments = dict(
        model=model, 
        template_name='registry/object_form.html',
        fields=[field.name for field in model._meta.fields[1:] if field.editable],
        success_url=reverse('registry:object_list', kwargs={'model_name': model_name}),   
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
