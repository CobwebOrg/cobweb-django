from django.contrib import admin
from reversion.admin import VersionAdmin

from archives import models

       
class CollectionInline(admin.TabularInline):
    model = models.Collection
    extra = 0
    show_change_link = True

    fields = [ 'name', 'identifier' ]
    readonly_fields = fields

class ClaimInline(admin.TabularInline):
    model = models.Claim
    extra = 0
    show_change_link = True
    
    fields = [ 
        'resource', 
        'collection', 
        'start_date', 
        'end_date', 
    ]
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