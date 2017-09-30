import reversion
from sys import stderr, stdout

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from sickle import Sickle

from archives.models import Collection, Holding
from core.models import Organization
from metadata.models import MDVocabulary, MDProperty, Metadatum
from webresources.models import nocrypto_url

from datasources.importers import importers


@reversion.register()
class APIEndpoint(models.Model):
    location = models.URLField(max_length=200, unique=True)
    organization = models.ForeignKey('core.Organization', 
            null=True, blank=True)

    importer_class_name = models.TextField( default = 'OAIPMHImporter',
            choices = [(name, name) for name in importers.keys()],
        )

    agent = models.OneToOneField(settings.AUTH_USER_MODEL, editable=False,
        null=True, blank=True)

    metadata = models.ManyToManyField('metadata.Metadatum', blank=True)

    @classmethod
    def get_archiveit_root(cls,):
        return cls.objects.get_or_create(
            location = 'https://archive-it.org/oai',
            defaults = {
                'importer_class_name': 'AITCollectionsImporter',
                'organization': Organization.objects.get_or_create(
                    identifier='http://archive-it.org/',
                    defaults={'name': "Archive-It.org"}
                )[0],
            }
        )[0]

    def get_importer(self):
        return importers[self.importer_class_name](self)

    def harvest(self):
        self.get_importer().harvest()

    def get_agent(self):
        if not self.agent:
            self.agent = get_user_model().objects.get_or_create(
                username = "APIEndpoint_agent_{}".format(self.id)
            )[0]
        return self.agent

    def __str__(self):
        return self.location or 'APIEndpoint {}'.format(self.pk)
