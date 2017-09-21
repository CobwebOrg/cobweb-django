from django.core.management.base import BaseCommand, CommandError
from math import inf
from sickle import Sickle
from sys import stderr
import re

from cobweb import models

SOFTWARE = models.Software.objects.get_or_create(name="Archive-It Importer")[0]
USER = models.User.objects.get_or_create(username="admin")[0]
AGENT = models.Agent.objects.get_or_create(user=USER, software=SOFTWARE)[0]
APIROOT = 'https://archive-it.org/oai/organizations/'
PROTOCOL = models.APIProtocol.objects.get_or_create(
    name = "OAI-PMH",
    identifier = "https://support.archive-it.org/hc/en-us/articles/210510506-Access-web-archives-with-the-OAI-PMH-metadata-feed",
    )[0]



def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def get_collection(record):
    if len(record.header.setSpecs) == 1 and record.header.setSpecs[0][:11] == 'collection:':
        id_number = record.header.setSpecs[0][11:] # actually should be string
        return "http://archive-it.org/collections/{}".format(id_number)
    else:
        eprint(record.header.identifier, record.header.setSpecs)
        raise ValueError("Can't find collection from setspecs.")

def only_one(list_object):
    """If list_object has exactly 1 item, returns it. Otherwise raises ValueError"""
    if len(list_object) == 1:
        return list_object[0]
    else:
        raise ValueError("Expected a list with exactly one item")

wayback_url_parser = re.compile('http\:\/\/wayback\.archive\-it\.org\/\d+\/\*/(https?\:\/\/.*)')
def parse_wayback_url(wayback_url):
    try:
        return models.nocrypto_url( 
            wayback_url_parser
            .match(wayback_url)
            .groups()[0] 
        )
    except:
        return wayback_url    

class Command(BaseCommand):
    help = 'Crudely imports some data about resources from Archive-It Parter Organizations'

    # collection_list_query = "https://archive-it.org/oai?verb=ListRecords&metadataPrefix=oai_dc"
    # sample_collection_query = "https://archive-it.org/oai/organizations/1036?verb=ListRecords&metadataPrefix=oai_dc&resumptionToken=0,447"

    def handle(self, *args, **kwargs):
        for api in PROTOCOL.apiendpoint_set.filter(url__startswith=APIROOT):
            print(api)
            self.harvest_organization(api)

    def harvest_organization(self, api):
        try:
            ait = Sickle(api.identifier)
            records = ait.ListRecords(metadataPrefix='oai_dc')
            for record in records:
                root_url = parse_wayback_url(record.header.identifier)
                
                collection_uri = get_collection(record)
                collection = models.Collection.objects.get_or_create(
                    identifier=collection_uri,
                    defaults={
                        'name': "Autogenerated Collection for {}".format(collection_uri),
                        'institution': api.institution,
                    }
                )[0]

                resource = models.Resource.objects.get_or_create(
                    location=models.nocrypto_url(root_url)[0]

                holding = models.Holding.objects.get_or_create(
                    resource=resource,
                    collection=collection,
                    asserted_by=AGENT,
                )[0]

                holding.raw_metadata = record.raw

                # for tag_property, tag_values in record.metadata.items():
                #     for tag_value in tag_values:
                #         try:
                #             collection.tags.add(
                #                 models.Tag.objects.get_or_create(
                #                     tag_property=tag_property,
                #                     tag_value=tag_value
                #                 )[0]
                #             )
                #         except Exception as ex:
                #             eprint(ex, type(ex))

                holding.full_clean()
                holding.save()
        except Exception as ex:
            eprint(type(ex), ex)

