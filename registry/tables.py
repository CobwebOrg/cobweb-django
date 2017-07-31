import django_tables2

from django.urls import reverse

from . import models



class InstitutionTable(django_tables2.Table):
    class Meta:
        model = models.Institution
        
class AgentTable(django_tables2.Table):
    class Meta:
        model = models.Agent
        
class ProjectTable(django_tables2.Table):
    name = django_tables2.TemplateColumn(
        """<a href="{% url 'registry:project_detail' pk=record.id %}">
            {{ record.name }}
        </a>"""
    )
    
    class Meta:
        model = models.Project
        row_attrs = {
            'class': 'clickable-row',
            'data-href': lambda record: reverse(
                'registry:project_detail',
                kwargs={'pk': record.pk}
            )
        }
        attrs = {'class': 'table table-hover'}
        fields = ('name', 'description')

class SeedTable(django_tables2.Table):
    # use default Column instead of URL render as a clickable link
    url = django_tables2.Column()
    
    class Meta:
        model = models.Seed
        attrs = {'class': 'table table-hover'}
        fields = ('url', 'description', 'created', 'nominated_by')
        
class ClaimTable(django_tables2.Table):
    class Meta:
        model = models.Claim
        
class HoldingTable(django_tables2.Table):
    class Meta:
        model = models.Holding