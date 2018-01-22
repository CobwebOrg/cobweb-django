from django.contrib import admin
from reversion.admin import VersionAdmin

from datasources.models import APIEndpoint


class APIEndpointInline(admin.TabularInline):
    model = APIEndpoint
    extra = 0
    show_change_link = True

    fields = [ 'location', 'importer_class_name' ]
    readonly_fields = fields

@admin.register(APIEndpoint)
class APIEndpointAdmin(VersionAdmin):
    fields = ['location', 'organization', 'last_updated', 'importer_class_name']
    readonly_fields = ['last_updated']
