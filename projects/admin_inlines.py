from django.contrib import admin

from projects.models import Nomination, Project


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0
    show_change_link = True

    fields = ['title', 'keywords']
    readonly_fields = fields


class NominationInline(admin.TabularInline):
    model = Nomination
    extra = 0
    show_change_link = True

    fields = ['resource', 'project', 'nominated_by']
    readonly_fields = fields
