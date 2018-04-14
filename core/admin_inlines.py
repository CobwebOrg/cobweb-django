from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from core.models import Note, ResourceDescription, ResourceScan


class NoteInline(GenericStackedInline):
    model = Note
    fields = ('when_created', 'author', 'visibility', 'text')
    readonly_fields = ('when_created',)
    extra = 0

class ResourceDescriptionInline(admin.StackedInline):
    model = ResourceDescription
    extra = 0

class ResourceScanInline(admin.StackedInline):
    model = ResourceScan
    extra = 0
