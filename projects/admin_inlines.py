from django.contrib import admin

from projects.models import Nomination, Project, Claim


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

    fields = ['resource', 'project']
    readonly_fields = fields


class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 0
    show_change_link = True

    fields = [
        'resource',
        'collection',
        'start_date',
        'end_date',
    ]
    readonly_fields = fields
