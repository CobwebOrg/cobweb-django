from django.contrib import admin, auth
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.admin import GenericTabularInline
from reversion.admin import VersionAdmin

from archives.admin import CollectionInline
from metadata.admin import MetadatumInline

from core import models


admin.site.unregister(auth.models.Group)

@admin.register(get_user_model())
class UserAdmin(VersionAdmin, auth.admin.UserAdmin):
    pass
    
@admin.register(models.Organization)
class OrganizationAdmin(VersionAdmin):
    filter_horizontal = [ 'metadata' ]
    # fields = ['name', 'address']
    inlines = [ CollectionInline ]
