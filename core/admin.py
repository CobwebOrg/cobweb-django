from django.contrib import admin, auth
from reversion.admin import VersionAdmin

from webarchives.admin import APIEndpointInline

from core import models
from core.admin_inlines import NoteInline
from projects.admin_inlines import NominationInline

admin.site.unregister(auth.models.Group)


@admin.register(models.User)
class UserAdmin(VersionAdmin, auth.admin.UserAdmin):
    model = models.User

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    inlines = (NoteInline,)


@admin.register(models.Organization)
class OrganizationAdmin(VersionAdmin):
    pass
    # inlines = [APIEndpointInline, NoteInline]


@admin.register(models.Note)
class NoteAdmin(VersionAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(VersionAdmin):
    model = models.Tag
    # inlines = [ ProjectInline ]


@admin.register(models.Resource)
class ResourceAdmin(VersionAdmin):
    model = models.Resource
    inlines = (NominationInline, NoteInline)
