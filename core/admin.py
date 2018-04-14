from django.contrib import admin, auth
from reversion.admin import VersionAdmin

from archives.admin_inlines import CollectionInline
from datasources.admin import APIEndpointInline

from core import models


admin.site.unregister(auth.models.Group)


@admin.register(auth.get_user_model())
class UserAdmin(VersionAdmin, auth.admin.UserAdmin):
    pass


@admin.register(models.Organization)
class OrganizationAdmin(VersionAdmin):
    inlines = [CollectionInline, APIEndpointInline]


@admin.register(models.Tag)
class TagAdmin(VersionAdmin):
    model = models.Tag
    # inlines = [ ProjectInline ]
