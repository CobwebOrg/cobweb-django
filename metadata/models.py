import reversion
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.


class MetadataJSONField(JSONField):
    pass


@reversion.register()
class Keyword(models.Model):
    """A single keyword."""

    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        """Return keyword as string."""
        return self.name


class CobwebMetadataMixin(models.Model):
    """The standard metadata fields attached to the main data types."""

    title = models.TextField(null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    metadata = MetadataJSONField(null=True, blank=True)

    class Meta:
        abstract = True
