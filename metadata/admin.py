from django.contrib import admin
from reversion.admin import VersionAdmin

# from datasources.admin import APIEndpointInline
# from core.admin import OrganizationInline
from projects.admin import NominationInline
from archives.admin_inlines import CollectionInline, ClaimInline, HoldingInline

from metadata import models, admin_inlines



@admin.register(models.MDVocabulary)
class MDVocabularyAdmin(VersionAdmin):
    model = models.MDVocabulary
    inlines = [ admin_inlines.MDPropertyInline ]

@admin.register(models.MDProperty)
class MDPropertyAdmin(VersionAdmin):
    model = models.MDProperty
    inlines = [ admin_inlines.MetadatumInline ]

@admin.register(models.Metadatum)
class MetadatumAdmin(VersionAdmin):
    # inlines = []
    pass
