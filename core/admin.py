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
    search_fields = ['first_name', 'last_name', 'email']
    inlines = (NoteInline,)


@admin.register(models.Organization)
class OrganizationAdmin(VersionAdmin):
    fieldsets = (
        (None, {'fields': ('slug', 'full_name', 'short_name',
                           'parent_organization', 'description')}),
        ('People', {'fields': ('administrators', 'contact')}),
        ('Contact', {'fields': ('address', 'telephone_number', 'url', 'email_address',
                                'identifier')}),
    )
    autocomplete_fields = ['parent_organization', 'administrators', 'contact']
    search_fields = ['slug', 'short_name', 'full_name']
    readonly_fields = ['slug', 'identifier']
    inlines = [APIEndpointInline, NoteInline]


@admin.register(models.Note)
class NoteAdmin(VersionAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(VersionAdmin):
    model = models.Tag
    search_fields = ['Name']
    # inlines = [ ProjectInline ]


@admin.register(models.Resource)
class ResourceAdmin(VersionAdmin):
    model = models.Resource
    fields = ['url']
    readonly_fields = ['url']
    inlines = (NominationInline, NoteInline)
    autocomplete_fields = ['language']
