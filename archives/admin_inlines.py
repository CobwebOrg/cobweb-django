from django.contrib import admin

from archives import models


class CollectionInline(admin.TabularInline):
    model = models.Collection
    extra = 0
    show_change_link = True

    fields = ['title', 'identifier']
    readonly_fields = fields


class HoldingInline(admin.TabularInline):
    model = models.Holding
    extra = 0
    show_change_link = True

    fields = [
        'resource',
        'collection',
    ]
    readonly_fields = fields
