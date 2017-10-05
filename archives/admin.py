from django.urls import reverse
from django.contrib import admin
from django.contrib.postgres import fields as postgres_fields
from django_json_widget.widgets import JSONEditorWidget
from reversion.admin import VersionAdmin

from archives import models, admin_inlines
from metadata.admin_inlines import MetadatumBaseInline


       

class CollectionMDAdminInline(MetadatumBaseInline):
    model = models.Collection.metadatums.through

class ClaimMDAdminInline(MetadatumBaseInline):
    model = models.Claim.metadatums.through

class HoldingMDAdminInline(MetadatumBaseInline):
    model = models.Holding.metadatums.through



@admin.register(models.Collection)  
class CollectionAdmin(VersionAdmin):
    inlines = [ 
        # CollectionMDAdminInline,
        admin_inlines.ClaimInline,
        admin_inlines.HoldingInline,
    ]
    exclude = [ 'metadatums' ]

    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(models.Claim)
class ClaimAdmin(VersionAdmin):
    inlines = [ ClaimMDAdminInline ]

    exclude = [ 'metadatums' ]

    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(models.Holding)
class HoldingAdmin(VersionAdmin):
    inlines = [ HoldingMDAdminInline ]
    readonly_fields = [ 'resource_link', 'created' ]

    exclude = [ 'metadatums' ]

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
        'resource_link', 
        'collection',
        'raw_metadata',
        'created',
        'deprecated',
    ]