from django.contrib import admin

from projects.models import Nomination, Project, Claim


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0
    show_change_link = True

    fields = ['title', 'tags']
    readonly_fields = fields


class NominationInline(admin.TabularInline):
    model = Nomination
    extra = 0
    show_change_link = True

    fields = ['title', 'resource', 'project']
    # readonly_fields = fields


class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 0
    show_change_link = True

    fields = [
        'project',
        'resource',
        'organization',
    ]
    readonly_fields = fields
