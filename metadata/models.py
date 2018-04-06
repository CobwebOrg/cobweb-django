import reversion
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.


class MetadataJSONField(JSONField):
    pass


@reversion.register()
class Tag(models.Model):
    """A single tag."""

    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self) -> str:
        """Return tag as string."""
        return self.name


class CobwebMetadataMixin(models.Model):
    """The standard metadata fields attached to the main data types."""

    title = models.TextField(null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    metadata = MetadataJSONField(null=True, blank=True)

    class Meta:
        abstract = True
