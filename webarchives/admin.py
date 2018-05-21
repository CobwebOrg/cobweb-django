from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin

from webarchives import models


class APIEndpointInline(admin.TabularInline):
    model = models.APIEndpoint
    extra = 0
    show_change_link = True

    fields = [ 'location', 'importer_class_name' ]
    readonly_fields = fields

@admin.register(models.APIEndpoint)
class APIEndpointAdmin(admin.ModelAdmin):
    pass
    # fields = ['location', 'organization', 'last_updated', 'importer_class_name']
    # readonly_fields = ['last_updated']

@admin.register(models.ImportedRecord)
class ImportedRecordAdmin(admin.ModelAdmin):
    pass