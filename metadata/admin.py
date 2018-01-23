from django.contrib import admin
from django.contrib.postgres import fields as postgres_fields
from reversion.admin import VersionAdmin

from metadata import models


class MetadataAdminMixin:
    fields = ['description', 'keywords', 'metadata']


@admin.register(models.Keyword)
class KeywordAdmin(VersionAdmin):
    model = models.Keyword
    # inlines = [ ProjectInline ]
