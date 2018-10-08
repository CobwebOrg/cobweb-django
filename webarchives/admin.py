from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin

from webarchives import models


class APIEndpointInline(admin.TabularInline):
    model = models.APIEndpoint
    extra = 0
    show_change_link = True
    fields = ['organization', 'url', 'last_updated']
    autocomplete_fields = ['organization']
    readonly_fields = ['last_updated']

@admin.register(models.APIEndpoint)
class APIEndpointAdmin(admin.ModelAdmin):
    fields = ['organization', 'url', 'last_updated']
    autocomplete_fields = ['organization']
    readonly_fields = ['last_updated']

@admin.register(models.ImportedRecord)
class ImportedRecordAdmin(admin.ModelAdmin):
    fields = ['source_feed', 'identifier', 'metadata', 'record_type',
              'resource', 'parents']
    readonly_fields = fields
