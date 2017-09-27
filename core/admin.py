from django.contrib import admin, auth
from reversion.admin import VersionAdmin

from archives.admin import CollectionInline
from metadata.admin import MetadatumInline

from core import models


class AgentInline(admin.TabularInline):
    model = models.Agent
    extra = 0
    fields = [ 'user', 'software', ]

    

# class AgentIdentifierInline(admin.TabularInline):
#     model = models.AgentIdentifier
#     extra = 0
#     fields = ['id_type', 'value']


@admin.register(models.Agent)
class AgentAdmin(VersionAdmin):
    pass


admin.site.unregister(auth.models.Group)

@admin.register(models.User)
class UserAdmin(VersionAdmin, auth.admin.UserAdmin):
    inlines = [ AgentInline ]

@admin.register(models.Software)
class SoftwareAdmin(VersionAdmin):
    inlines = [ AgentInline ]

@admin.register(models.Organization)
class OrganizationAdmin(VersionAdmin):
    filter_horizontal = [ 'metadata' ]
    inlines = [ CollectionInline ]
