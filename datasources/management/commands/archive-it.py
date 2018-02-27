from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
import random

from datasources.models import APIEndpoint


class Command(BaseCommand):
    help = 'Tells each APIEndpoint instance to harvest data.'

    def handle(self, *args, **kwargs):
        cutoff_datetime = timezone.now()

        APIEndpoint.get_archiveit_root().harvest()

        for api in APIEndpoint.objects.filter(Q(last_updated__lt=cutoff_datetime)
                                              | Q(last_updated=None)):
            try:
                api.harvest()
            except Exception as ex:
                pass
