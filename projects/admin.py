from django.urls import reverse
from django.contrib import admin
from reversion.admin import VersionAdmin

from projects.models import Nomination, Project


class NominationInline(admin.TabularInline):
    model = Nomination
    extra = 0
    
    def changeform_link(self, instance):
        if instance.id:
            changeform_url = reverse('admin:projects_nomination_change', args=(instance.id,))
            return '<a href="{changeform_url}" target="_blank">Edit</a>'.format(
                changeform_url = changeform_url,
            )
        else:
            return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header
    
    fields = [ 'changeform_link', 'resource', 'project', 'nominated_by' ]
    readonly_fields = fields



@admin.register(Project)
class ProjectAdmin(VersionAdmin):
    inlines = [ NominationInline ]

@admin.register(Nomination)
class NominationAdmin(VersionAdmin):
    pass
