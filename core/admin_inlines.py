from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from core.models import Organization, Note, CrawlScope


class OrganizationInline(admin.TabularInline):
    model = Organization


class NoteInline(GenericStackedInline):
    model = Note
    fields = ('when_created', 'author', 'visibility', 'text')
    readonly_fields = ('when_created',)
    extra = 0


class CrawlScopeInline(admin.StackedInline):
    model = CrawlScope
    extra = 0
