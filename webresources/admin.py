from django.contrib import admin
from reversion.admin import VersionAdmin

from projects.admin import NominationInline
from archives.admin import ClaimInline, HoldingInline

from webresources.models import Resource

@admin.register(Resource)
class ResourceAdmin(VersionAdmin):
    inlines = [ NominationInline, ClaimInline, HoldingInline ]