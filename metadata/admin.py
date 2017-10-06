from django.contrib import admin
from reversion.admin import VersionAdmin

# from datasources.admin import APIEndpointInline
# from core.admin import OrganizationInline
from projects.admin_inlines import ProjectInline
# from archives.admin_inlines import CollectionInline, ClaimInline, HoldingInline

from metadata import models



@admin.register(models.Keyword)
class KeywordAdmin(VersionAdmin):
    model = models.Keyword
    # inlines = [ ProjectInline ]

