from django.contrib import admin
from reversion.admin import VersionAdmin

from projects.models import Nomination, Project, Claim
from projects.admin_inlines import NominationInline


@admin.register(Project)
class ProjectAdmin(VersionAdmin):
    inlines = [NominationInline]
    filter_horizontal = ['keywords', 'administrators', 'nominators']


@admin.register(Nomination)
class NominationAdmin(VersionAdmin):
    pass


@admin.register(Claim)
class ClaimAdmin(VersionAdmin):
    pass
