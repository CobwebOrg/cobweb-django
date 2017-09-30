from django.contrib import admin
from reversion.admin import VersionAdmin

from metadata.admin import MetadatumInline

from datasources.models import APIEndpoint


class APIEndpointInline(admin.TabularInline):
    model = APIEndpoint
    extra = 0
    show_change_link = True

    # fields = [ 'name', 'identifier' ]
    # readonly_fields = fields

@admin.register(APIEndpoint)
class APIEndpointAdmin(VersionAdmin):
    filter_horizontal = [ 'metadata' ]
