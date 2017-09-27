from django.contrib import admin
from reversion.admin import VersionAdmin

from metadata import models

# Register your models here.

class MDVocabularyInline(admin.TabularInline):
    model = models.MDVocabulary
    extra = 0
    show_change_link = True

class MDPropertyInline(admin.TabularInline):
    model = models.MDProperty
    extra = 0
    show_change_link = True

class MetadatumInline(admin.TabularInline):
    model = models.Metadatum
    extra = 0
    show_change_link = True

@admin.register(models.MDVocabulary)
class MDVocabularyAdmin(VersionAdmin):
    model = models.MDVocabulary
    inlines = [ MDPropertyInline ]

@admin.register(models.MDProperty)
class MDPropertyAdmin(VersionAdmin):
    model = models.MDProperty
    inlines = [ MetadatumInline ]

@admin.register(models.Metadatum)
class MetadatumAdmin(VersionAdmin):
    pass



# admin.site.register(
#     Node,
#     DraggableMPTTAdmin,
#     list_display=(
#         'tree_actions',
#         'indented_title',
#         # ...more fields if you feel like it...
#     ),
#     list_display_links=(
#         'indented_title',
#     ),
# )