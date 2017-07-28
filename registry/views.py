from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views import generic
from django.apps import apps
from django.urls import reverse
from django.template.loader import render_to_string

from django_tables2 import Table, Column

from . import models


#
#   Inline Views
#
        
class InstitutionTable(Table):
    class Meta:
        model = models.Institution
        
class AgentTable(Table):
    class Meta:
        model = models.Agent
        
class ProjectTable(Table):
    class Meta:
        model = models.Project
        attrs = {'class': 'table table-hover'}
        fields = ('name', 'description')
    
    def render_name(self, record, value):
        # print(">>> ", record, dir(record))
        return '<a href="{url}">{name}</a>'.format(
            name=value,
            url=reverse('registry:project_detail', kwargs={'pk': record.pk})
        )

class SeedTable(Table):
    class Meta:
        model = models.Seed
        attrs = {'class': 'table table-hover'}
        fields = ('url', 'description', 'created', 'nominated_by')
        
class ClaimTable(Table):
    class Meta:
        model = models.Claim
        
class HoldingTable(Table):
    class Meta:
        model = models.Holding
        
table_class_key = {
    models.Institution: InstitutionTable,
    models.Agent: AgentTable,
    models.Project: ProjectTable,
    models.Seed: SeedTable,
    models.Claim: ClaimTable,
    models.Holding: HoldingTable,
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
