from django.contrib import admin, auth
from reversion.admin import VersionAdmin

from archives.admin_inlines import CollectionInline
from datasources.admin import APIEndpointInline
from metadata.admin_inlines import MetadatumBaseInline

from core import models


class OrganizationMDInline(MetadatumBaseInline):
    model = models.Organization.metadata.through


admin.site.unregister(auth.models.Group)

@admin.register(auth.get_user_model())
class UserAdmin(VersionAdmin, auth.admin.UserAdmin):
    pass
    
@admin.register(models.Organization)
class OrganizationAdmin(VersionAdmin):
    inlines = [ OrganizationMDInline, CollectionInline, APIEndpointInline ]
    exclude = ['metadata']