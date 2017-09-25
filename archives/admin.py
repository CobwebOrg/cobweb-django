from django.urls import reverse
from django.contrib import admin
from reversion.admin import VersionAdmin

from archives import models


       
class CollectionInline(admin.TabularInline):
    model = models.Collection
    extra = 0
    def changeform_link(self, instance):
        if instance.id:
            return '<a href="{changeform_url}" target="_blank">{name}</a>'.format(
                changeform_url = reverse('admin:archives_collection_change', args=(instance.id,)),
                name = str(instance),
            )
        else:
            return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = 'Collection'

    fields = [ 'changeform_link', 'identifier' ]
    readonly_fields = fields

class ClaimInline(admin.TabularInline):
    model = models.Claim
    extra = 0
    
    def changeform_link(self, instance):
        if instance.id:
            changeform_url = reverse('admin:archives_claim_change', args=(instance.id,))
            return '<a href="{changeform_url}" target="_blank">Edit</a>'.format(
                changeform_url = changeform_url,
            )
        else:
            return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header
    
    fields = [ 
        'changeform_link', 
        'resource', 
        'collection', 
        'start_date', 
        'end_date', 
    ]
    readonly_fields = fields

class HoldingInline(admin.TabularInline):
    model = models.Holding
    extra = 0

    
    readonly_fields = [ 'changeform_link' ]
    
    def changeform_link(self, instance):
        if instance.id:
            changeform_url = reverse('admin:archives_holding_change', args=(instance.id,))
            return '<a href="{changeform_url}" target="_blank">Edit</a>'.format(
                changeform_url = changeform_url,
            )
        else:
            return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header
    
    fields = [
        'changeform_link', 
        'resource', 
        'collection',
    ]
    readonly_fields = fields



@admin.register(models.Collection)  
class CollectionAdmin(VersionAdmin):
    inlines = [ ClaimInline, HoldingInline ]

@admin.register(models.Claim)
class ClaimAdmin(VersionAdmin):
    pass

@admin.register(models.Holding)
class HoldingAdmin(VersionAdmin):
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