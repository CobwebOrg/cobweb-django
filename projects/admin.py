from django.contrib import admin
from reversion.admin import VersionAdmin

from core.admin_inlines import NoteInline, CrawlScopeInline
from projects.models import Nomination, Project, Claim
from projects.admin_inlines import NominationInline


@admin.register(Project)
class ProjectAdmin(VersionAdmin):
    search_fields = ['title', 'slug']
    autocomplete_fields = [
        'administrators',
        'nominator_orgs',
        'nominators',
        'nominator_blacklist',
        'tags',
        'subject_headings',
    ]
    # inlines = [NominationInline, NoteInline]


@admin.register(Nomination)
class NominationAdmin(VersionAdmin):
    autocomplete_fields = [
        'resource',
        'project',
        'language',
        'tags',
        'subject_headings',
    ]
    search_fields = ['project', 'resource', 'title']
    inlines = [NoteInline]


@admin.register(Claim)
class ClaimAdmin(VersionAdmin):
    autocomplete_fields = [
        'nomination',
        'organization',
        'imported_record',
    ]
    inlines = [NoteInline]
