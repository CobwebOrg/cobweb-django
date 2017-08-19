from django.urls import reverse
from django.contrib import admin

from . import models


class NominationInline(admin.TabularInline):
    model = models.Nomination
    extra = 0

    readonly_fields = [ 'changeform_link' ]
    
    def changeform_link(self, instance):
        if instance.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = reverse(
                'admin:nomination_change', args=(instance.id,)
            )
            return u'<a href="%s" target="_blank">Edit</a>' % changeform_url
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header
    
    fields = [ 'changeform_link', 'url', 'nominated_by', 'description', ]
    
class ClaimInline(admin.TabularInline):
    model = models.Claim
    extra = 0
    
    readonly_fields = [ 'created' ]
    fields = [ 
        'asserted_by', 
        'resource', 
        'institution', 
        'start_date', 
        'end_date', 
        # frequency, 
        'max_links', 
        # host_limit, 
        'time_limit', 
        'document_limit', 
        'data_limit', 
        'robot_exclusion_override', 
        # capture_software, 
        'created', 
        'deprecated', 
    ]
       
class HoldingInline(admin.TabularInline):
    model = models.Holding
    extra = 0
    
    readonly_fields = [ 'created' ]
    fields = [
        'asserted_by', 
        'resource', 
        'institution', 
        'created', 
        'deprecated', 
    ]


# class ProjectAdmin(admin.ModelAdmin):
#     inlines = [ NominationInline ]
#
# class NominationAdmin(admin.ModelAdmin):
#     inlines = [ ClaimInline, HoldingInline ]


admin.site.register(models.Institution)
admin.site.register(models.Agent)
admin.site.register(models.Project) #, ProjectAdmin)
admin.site.register(models.Collection)
admin.site.register(models.Resource)
admin.site.register(models.Nomination) #, NominationAdmin)
admin.site.register(models.Claim)
admin.site.register(models.Holding)