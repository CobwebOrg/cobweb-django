from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import random

from datasources import models


class Command(BaseCommand):
    help = 'Tells each APIEndpoint instance to harvest data.'

    def handle(self, *args, **kwargs):
        archiveit = models.APIEndpoint.get_archiveit_root()
        if models.APIEndpoint.objects.all().count() <= 1:
            archiveit.harvest()

        print("picking a random APIEndpoint...")
        api_endpoints = [ api for api in models.APIEndpoint.objects.all()
            if api != archiveit ]

        random.choice(api_endpoints).harvest()

        # for api in models.APIEndpoint.objects.all():
        #     print("Trying {} API at {}".format(api.organization, api))
        #     api.harvest()