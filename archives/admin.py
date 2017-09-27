from django.urls import reverse
from django.contrib import admin
from reversion.admin import VersionAdmin

from archives import models


       
class CollectionInline(admin.TabularInline):
    model = models.Collection
    extra = 0
    show_change_link = True

    fields = [ 'name', 'identifier' ]
    readonly_fields = fields

class ClaimInline(admin.TabularInline):
    model = models.Claim
    extra = 0
    show_change_link = True
    
    fields = [ 
        'resource', 
        'collection', 
        'start_date', 
        'end_date', 
    ]
    readonly_fields = fields

class HoldingInline(admin.TabularInline):
    model = models.Holding
    extra = 0
    show_change_link = True
    
    fields = [
        'resource', 
        'collection',
    ]
    readonly_fields = fields



@admin.register(models.Collection)  
class CollectionAdmin(VersionAdmin):
    filter_horizontal = [ 'metadata' ]
    inlines = [ ClaimInline, HoldingInline ]

@admin.register(models.Claim)
class ClaimAdmin(VersionAdmin):
    filter_horizontal = [ 'metadata' ]

@admin.register(models.Holding)
class HoldingAdmin(VersionAdmin):
    filter_horizontal = [ 'metadata' ]
    readonly_fields = [ 'resource_link', 'created' ]
    
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