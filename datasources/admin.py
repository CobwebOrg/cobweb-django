from django.contrib import admin
from reversion.admin import VersionAdmin

from datasources.models import APIEndpoint, APIProtocol


@admin.register(APIEndpoint)
class APIEndpointAdmin(VersionAdmin):
    pass

@admin.register(APIProtocol)
class APIProtocolAdmin(VersionAdmin):
    pass