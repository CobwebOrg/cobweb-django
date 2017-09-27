from django.urls import reverse
from django.contrib import admin
from reversion.admin import VersionAdmin

from projects.models import Nomination, Project


class NominationInline(admin.TabularInline):
    model = Nomination
    extra = 0
    show_change_link = True
    
    fields = [ 'resource', 'project', 'nominated_by' ]
    readonly_fields = fields



@admin.register(Project)
class ProjectAdmin(VersionAdmin):
    inlines = [ NominationInline ]

@admin.register(Nomination)
class NominationAdmin(VersionAdmin):
    pass
