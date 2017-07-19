from django.urls import reverse
from django.contrib import admin

from .models import Institution, Agent, Project, Seed, Claim, Holding


class SeedInline(admin.TabularInline):
    model = Seed
    extra = 0

    readonly_fields = [ 'changeform_link' ]
    
    def changeform_link(self, instance):
        if instance.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = reverse(
                'admin:registry_seed_change', args=(instance.id,)
            )
            return u'<a href="%s" target="_blank">Edit</a>' % changeform_url
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header
    
    fields = [ 'changeform_link', 'url', 'nominated_by', 'description', ]
    
class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 0
    
    readonly_fields = [ 'created' ]
    fields = [ 
        'asserted_by', 
        'seed', 
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
    model = Holding
    extra = 0
    
    readonly_fields = [ 'created' ]
    fields = [
        'asserted_by', 
        'seed', 
        'institution', 
        'created', 
        'deprecated', 
    ]


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ SeedInline ]

class SeedAdmin(admin.ModelAdmin):
    inlines = [ ClaimInline, HoldingInline ]


admin.site.register(Institution)
admin.site.register(Agent)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Seed, SeedAdmin)
admin.site.register(Claim)
admin.site.register(Holding)