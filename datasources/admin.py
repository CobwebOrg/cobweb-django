from django.contrib import admin
from reversion.admin import VersionAdmin

# from metadata.admin_inlines import MetadatumBaseInline

from datasources.models import APIEndpoint
from metadata.admin_inlines import MetadatumBaseInline


class APIEndpointMDInline(MetadatumBaseInline):
    model = APIEndpoint.metadata.through

class APIEndpointInline(admin.TabularInline):
    model = APIEndpoint
    extra = 0
    show_change_link = True

    fields = [ 'location', 'importer_class_name', 'metadata' ]
    readonly_fields = fields

@admin.register(APIEndpoint)
class APIEndpointAdmin(VersionAdmin):
    fields = ['location', 'organization', 'last_updated', 'importer_class_name']
    readonly_fields = ['last_updated']
    inlines = [ APIEndpointMDInline ]