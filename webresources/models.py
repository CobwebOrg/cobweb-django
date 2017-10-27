import reversion
from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from itertools import chain
from surt import handyurl
from urllib.parse import urlparse
from surt.DefaultIAURLCanonicalizer import canonicalize

validate_url = URLValidator()

def normalize_url(url):
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

    projects = models.ManyToManyField(
        'projects.Project',
        through='projects.Nomination',
        related_name='nominated_resources'
    )

    
    def __str__(self):
        return self.get_url()

    def get_resource_records(self):
        return chain(
            self.nominations.all(), 
            self.claims.all(), 
            self.holdings.all(),
        )

    def get_url(self):
    	return self.url or 'Resource {}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('webresources:detail', kwargs={'url': self.url})