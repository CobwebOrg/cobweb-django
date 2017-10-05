from django.contrib import admin
from django.contrib.postgres import fields as postgres_fields
from django_json_widget.widgets import JSONEditorWidget
from reversion.admin import VersionAdmin

# from metadata.admin_inlines import MetadatumBaseInline

from datasources.models import APIEndpoint
from metadata.admin_inlines import MetadatumBaseInline


class APIEndpointMDInline(MetadatumBaseInline):
    model = APIEndpoint.metadatums.through

class APIEndpointInline(admin.TabularInline):
    model = APIEndpoint
    extra = 0
    show_change_link = True

    fields = [ 'location', 'importer_class_name', 'metadatums' ]
    readonly_fields = fields

@admin.register(APIEndpoint)
class APIEndpointAdmin(VersionAdmin):
    fields = ['location', 'organization', 'last_updated', 'importer_class_name']
    readonly_fields = ['last_updated']
    inlines = [ APIEndpointMDInline ]
    exclude = [ 'metadatums' ]

    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }