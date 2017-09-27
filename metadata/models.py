from django.db import models

# Create your models here.

class MDVocabulary(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name='MDVocabulary'
        verbose_name_plural='MDVocabularies'

    def __str__(self):
        return self.name

class MDProperty(models.Model):
    vocabulary = models.ForeignKey(MDVocabulary, 
        null=True, blank=True, db_index=True)

    name = models.CharField(max_length=25, 
        null=True, blank=True, db_index=True)

    class Meta:
        unique_together = ('vocabulary', 'name')
        verbose_name='MDProperty'
        verbose_name_plural='MDProperties'

    def __str__(self):
        if self.vocabulary and self.name:
            return '{} : {}'.format(self.vocabulary, self.name)
        else:
            return self.name or str(self.vocabulary)

class Metadatum(models.Model):
    md_property = models.ForeignKey(MDProperty, 
        null=True, blank=True, db_index=True)

    name = models.CharField(max_length=25, db_index=True)

    class Meta:
        unique_together = ('md_property', 'name')

    def __str__(self):
        if self.md_property:
            return "{} : {}".format(self.md_property, self.name)
        else:
            return self.name

    