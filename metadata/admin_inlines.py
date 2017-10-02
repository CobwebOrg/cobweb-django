from django.contrib import admin

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

class MetadatumBaseInline(admin.TabularInline):
    # Use as a base class for specialized inline classes, e.g.:
    # class ModelMDInline(metadata.admin.MetadatumBaseInline): 
    #     model = Model.metadata.through

    extra = 0
    show_change_link = True

    def md_name(self, instance):
        if instance.id:
            return(str(instance.metadatum))
    md_name.short_description = 'Metadata'
    fields = [ 'md_name' ]
    readonly_fields = fields