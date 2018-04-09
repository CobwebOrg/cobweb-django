import typing

from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from itertools import chain
from surt import handyurl
from surt.DefaultIAURLCanonicalizer import canonicalize

validate_url = URLValidator()


def normalize_url(url: str) -> str:
    normalized_url = (
        canonicalize(handyurl.parse(url)).geturl()
        .replace('https://', 'http://')
        .replace('sftp://', 'ftp://')
    )
    validate_url(normalized_url)
    return normalized_url


class NormalizedURLField(models.URLField):
    """Subclass of URLField that maps https to http and sftp to ftp."""

    def clean(self, value, model_instance):
        return super().clean(normalize_url(value), model_instance)


class Resource(models.Model):
    url = NormalizedURLField(max_length=1000, null=False, blank=False,
                             unique=True)

    def __str__(self) -> str:
        return self.get_url()

    def get_resource_records(self) -> typing.Iterable:
        return chain(
            self.nominations.all(),
            self.tags.all(),
        )

    def get_url(self) -> str:
        return self.url or 'Resource {}'.format(self.pk)

    def get_absolute_url(self) -> str:
        return reverse('webresources:detail', kwargs={'url': self.url})

    def resource_record_count(self) -> int:
        return (
            self.nominations.count()
            + self.tags.count()
        )
