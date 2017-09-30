import reversion
from django.db import models

# Create your models here.

@reversion.register()
class MDVocabulary(models.Model):
    name = models.TextField(unique=True, db_index=True)

    class Meta:
        verbose_name='MDVocabulary'
        verbose_name_plural='MDVocabularies'

    def __str__(self):
        return self.name

@reversion.register()
class MDProperty(models.Model):
    vocabulary = models.ForeignKey(MDVocabulary, 
        null=True, blank=True, db_index=True)

    name = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        unique_together = ('vocabulary', 'name')
        verbose_name='MDProperty'
        verbose_name_plural='MDProperties'

    def __str__(self):
        if self.vocabulary and self.name:
            return '{} : {}'.format(self.vocabulary, self.name)
        else:
            return self.name or str(self.vocabulary)

@reversion.register()
class Metadatum(models.Model):
    md_property = models.ForeignKey(MDProperty, 
        null=True, blank=True, db_index=True)

    name = models.TextField(db_index=True)

    class Meta:
        unique_together = ('md_property', 'name')

    def __str__(self):
        if self.md_property:
            return "{} : {}".format(self.md_property, self.name)
        else:
            return self.name

    