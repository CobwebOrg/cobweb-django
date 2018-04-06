from django.contrib import admin
from django.contrib.postgres import fields as postgres_fields
from reversion.admin import VersionAdmin

from metadata import models


class MetadataAdminMixin:
    fields = ['description', 'tags', 'metadata']


@admin.register(models.Tag)
class TagAdmin(VersionAdmin):
    model = models.Tag
    # inlines = [ ProjectInline ]
