from django.contrib import admin, auth
from reversion.admin import VersionAdmin
from django.contrib.postgres import fields as postgres_fields
from django_json_widget.widgets import JSONEditorWidget

from archives.admin_inlines import CollectionInline
from datasources.admin import APIEndpointInline

from core import models


admin.site.unregister(auth.models.Group)

@admin.register(auth.get_user_model())
class UserAdmin(VersionAdmin, auth.admin.UserAdmin):
    pass
    
@admin.register(models.Organization)
class OrganizationAdmin(VersionAdmin):
    inlines = [ CollectionInline, APIEndpointInline ]

    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }