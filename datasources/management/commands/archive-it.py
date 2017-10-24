from django.core.management.base import BaseCommand, CommandError

from datasources import models


class Command(BaseCommand):
    help = 'Tells each APIEndpoint instance to harvest data.'

    def handle(self, *args, **kwargs):
        models.APIEndpoint.get_archiveit_root().harvest()
        ( models.APIEndpoint.objects
            .get(location='https://archive-it.org/oai/organizations/62')
            .harvest() )
        # for api in models.APIEndpoint.objects.all():
        #     print("Trying {} API at {}".format(api.organization, api))
        #     api.harvest()