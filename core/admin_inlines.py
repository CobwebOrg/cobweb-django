from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from core.models import Note


class NoteInline(GenericStackedInline):
    model = Note
    fields = ('when_created', 'author', 'visibility', 'text')
    readonly_fields = ('when_created',)
    extra = 0

