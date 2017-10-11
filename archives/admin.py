from django.urls import reverse
from django.contrib import admin
from django.contrib.postgres import fields as postgres_fields
from django_json_widget.widgets import JSONEditorWidget
from reversion.admin import VersionAdmin

from archives import models, admin_inlines

       
@admin.register(models.Collection)  
class CollectionAdmin(VersionAdmin):
    inlines = [ 
        admin_inlines.ClaimInline,
        admin_inlines.HoldingInline,
    ]

    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(models.Claim)
class ClaimAdmin(VersionAdmin):

    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(models.Holding)
class HoldingAdmin(VersionAdmin):
    readonly_fields = [ 'resource_link', 'created' ]

    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }
    
    def resource_link(self, instance):
        if instance.id:
            changeform_url = reverse('admin:webresources_resource_change', args=(instance.resource.id,))
            return '<a href="{changeform_url}" target="_blank">{resource}</a>'.format(
                changeform_url = changeform_url,
                resource = instance.resource,
            )
        else:
            return u''
    resource_link.allow_tags = True
    resource_link.short_description = 'Resource'
    
    fields = [
        'resource', 
        'collection',
        'raw_metadata',
        'created',
        'deprecated',
    ]