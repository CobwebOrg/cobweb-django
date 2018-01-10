from django.contrib import admin
from reversion.admin import VersionAdmin

from projects.admin_inlines import NominationInline, ClaimInline
from archives.admin_inlines import HoldingInline

from webresources.models import Resource


@admin.register(Resource)
class ResourceAdmin(VersionAdmin):
    inlines = [NominationInline, ClaimInline, HoldingInline]
