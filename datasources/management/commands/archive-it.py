from django.core.management.base import BaseCommand, CommandError
from math import inf
from sickle import Sickle
from sys import stderr

from archives.models import Collection
from core.models import Organization, User
from datasources import models
from webresources.models import nocrypto_url



class Command(BaseCommand):
    help = 'Tells each APIEndpoint instance to harvest data.'

    def handle(self, *args, **kwargs):
        # models.APIEndpoint.get_archiveit_root().harvest()
        for api in models.APIEndpoint.objects.all():
            print("Trying {} API at {}".format(api.organization, api))
            api.harvest()