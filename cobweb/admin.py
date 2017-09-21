
from django.urls import reverse
from django.contrib import admin, auth, contenttypes
from reversion.admin import VersionAdmin

from cobweb import models



class AgentInline(admin.TabularInline):
    model = models.Agent
    extra = 0
    fields = [ 'user', 'software', ]

class NominationInline(admin.TabularInline):
    model = models.Nomination
    extra = 0
    
    def changeform_link(self, instance):
        if instance.id:
            changeform_url = reverse('admin:cobweb_nomination_change', args=(instance.id,))
            return '<a href="{changeform_url}" target="_blank">Edit</a>'.format(
                changeform_url = changeform_url,
            )
        else:
            return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header
    
    fields = [ 'changeform_link', 'resource', 'project', 'nominated_by' ]
    readonly_fields = fields
    
class ClaimInline(admin.TabularInline):
    model = models.Claim
    extra = 0
    
    def changeform_link(self, instance):
        if instance.id:
            changeform_url = reverse('admin:cobweb_claim_change', args=(instance.id,))
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
        'asserted_by',
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
            changeform_url = reverse('admin:cobweb_holding_change', args=(instance.id,))
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
        'asserted_by',
    ]
    readonly_fields = fields

# class AgentIdentifierInline(admin.TabularInline):
#     model = models.AgentIdentifier
#     extra = 0
#     fields = ['id_type', 'value']


@admin.register(models.Agent)
class AgentAdmin(VersionAdmin):
    pass

@admin.register(models.APIEndpoint)
class APIEndpointAdmin(VersionAdmin):
    pass

@admin.register(models.APIProtocol)
class APIProtocolAdmin(VersionAdmin):
    pass

admin.site.unregister(auth.models.Group)

@admin.register(models.User)
class UserAdmin(VersionAdmin, auth.admin.UserAdmin):
    inlines = [ AgentInline ]

@admin.register(models.Software)
class SoftwareAdmin(VersionAdmin):
    inlines = [ AgentInline ]

@admin.register(models.Institution)
class InstitutionAdmin(VersionAdmin):
    # inlines = [  ]
    pass

@admin.register(models.Resource)
class ResourceAdmin(VersionAdmin):
    inlines = [ NominationInline, ClaimInline, HoldingInline ]

@admin.register(models.Project)
class ProjectAdmin(VersionAdmin):
    inlines = [ NominationInline ]

@admin.register(models.Nomination)
class NominationAdmin(VersionAdmin):
    pass

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
            changeform_url = reverse('admin:cobweb_resource_change', args=(instance.resource.id,))
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
        'asserted_by',
        'raw_metadata',
        'created',
        'deprecated',
    ]
