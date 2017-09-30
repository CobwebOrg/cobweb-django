from django.core.management.base import BaseCommand, CommandError
from math import inf
from sickle import Sickle
from sys import stderr

from archives.models import Collection
from core.models import Organization, User
from datasources import models
from webresources.models import nocrypto_url



class Command(BaseCommand):
    help = 'Crudely imports some data about Archive-It collections'

    def handle(self, *args, **kwargs):
        print("Initializing AIT")
        ait = models.APIEndpoint.get_archiveit_root()
        ait.harvest()
        