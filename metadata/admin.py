from django.contrib import admin
from django.contrib.postgres import fields as postgres_fields
from django_json_widget.widgets import JSONEditorWidget
from reversion.admin import VersionAdmin

# from datasources.admin import APIEndpointInline
# from core.admin import OrganizationInline
from projects.admin_inlines import ProjectInline
# from archives.admin_inlines import CollectionInline, ClaimInline, HoldingInline

from metadata import models



class MetadataAdminMixin:
    fields = ['description', 'keywords', 'metadata', 'raw_metadata']

    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(models.Keyword)
class KeywordAdmin(VersionAdmin):
    model = models.Keyword
    # inlines = [ ProjectInline ]

