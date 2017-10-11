import reversion
from django.db.models import Q
from django.db import models


def nocrypto_url(url):
    return( url
        .replace('https://', 'http://')
        .replace('sftp://', 'ftp://')
    )

class NocryptoURLField(models.URLField):
    """Subclass of URLField that maps https to http and sftp to ftp."""
    def clean(self, value, model_instance):
        return super().clean(nocrypto_url(value), model_instance)

@reversion.register()
class Resource(models.Model):
    location = NocryptoURLField(max_length=1000, null=False, blank=False, 
        unique=True)

    projects = models.ManyToManyField(
        'projects.Project',
        through='projects.Nomination',
        related_name='nominated_resources'
    )

    
    def __str__(self):
        return self.get_url()

    def get_url(self):
    	return self.location or 'Resource {}'.format(self.pk)