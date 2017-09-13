
from django.urls import reverse
from django.contrib import admin, auth, contenttypes

from . import models


class MetadataRecordAdmin(contenttypes.admin.GenericStackedInline):
    model = models.MetadataRecord
    extra = 0
    fields = [ 'asserted_by', 'metadata_type', 'metadata' ]

class AgentInline(admin.TabularInline):
    model = models.Agent
    extra = 0
    fields = [ 'user', 'software', ]

class NominationInline(admin.TabularInline):
    model = models.Nomination
    extra = 0

    readonly_fields = [ 'changeform_link' ]
    
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
    
    fields = [ 'changeform_link', 'resource', 'nominated_by', 'project', ]
    
class ClaimInline(admin.TabularInline):
    model = models.Claim
    extra = 0
    
    readonly_fields = [ 'changeform_link' ]
    
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

# class AgentIdentifierInline(admin.TabularInline):
#     model = models.AgentIdentifier
#     extra = 0
#     fields = ['id_type', 'value']
    

class UserAdmin(auth.admin.UserAdmin):
    inlines = [ AgentInline ]

class SoftwareAdmin(admin.ModelAdmin):
    inlines = [ AgentInline ]

class InstitutionAdmin(admin.ModelAdmin):
    inlines = [ MetadataRecordAdmin ]

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ NominationInline, MetadataRecordAdmin ]
    
class CollectionAdmin(admin.ModelAdmin):
    inlines = [ ClaimInline, HoldingInline, MetadataRecordAdmin ]

class ResourceAdmin(admin.ModelAdmin):
    inlines = [ NominationInline, ClaimInline, HoldingInline, MetadataRecordAdmin ]



admin.site.unregister(auth.models.Group)

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Software, SoftwareAdmin)
admin.site.register(models.Institution, InstitutionAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Resource, ResourceAdmin)
admin.site.register(models.Nomination)
admin.site.register(models.Claim)
admin.site.register(models.Holding)

admin.site.register(models.Agent)
admin.site.register(models.MetadataRecord)
admin.site.register(models.MetadataType)