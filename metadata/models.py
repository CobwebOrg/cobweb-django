import reversion
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.


@reversion.register()
class Keyword(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name


class CobwebMetadataMixin(models.Model):
    description = models.TextField('Description', null=True, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    metadata = JSONField(null=True, blank=True)
    raw_metadata = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
