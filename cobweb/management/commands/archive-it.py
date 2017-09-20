from django.core.management.base import BaseCommand, CommandError
from ipdb import set_trace
from math import inf
from sickle import Sickle
from sys import stderr

from cobweb import models

AIT_COLLECTIONS_API = "https://archive-it.org/oai"
SOFTWARE = models.Software.objects.get_or_create(name="Archive-It Importer")[0]
USER = models.User.objects.get_or_create(username="admin")[0]
AGENT = models.Agent.objects.get_or_create(user=USER, software=SOFTWARE)[0]
MDTYPE = models.MetadataType.objects.get_or_create(
    name = "Archive-It OAI-PMH oai_dc",
    url = "https://support.archive-it.org/hc/en-us/articles/210510506-Access-web-archives-with-the-OAI-PMH-metadata-feed",
    )[0]
PROTOCOL = models.APIProtocol.objects.get_or_create(
    name = "OAI-PMH",
    uri = "https://support.archive-it.org/hc/en-us/articles/210510506-Access-web-archives-with-the-OAI-PMH-metadata-feed",
    )[0]

# def ait_partner_records(organization_id):
#     return "https://archive-it.org/oai/organizations/{:04d}".format(organization_id)

def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def get_organization(record):
    if len(record.header.setSpecs) == 1 and record.header.setSpecs[0][:13] == 'organization:':
        id_number = record.header.setSpecs[0][13:] # actually should be string
        uri = "http://archive-it.org/organizations/{}".format(id_number)
        api_url = "https://archive-it.org/oai/organizations/{}".format(id_number)
        return uri, api_url
    else:
        eprint(record.header.identifier, record.header.setSpecs)
        raise ValueError("Can't find organization from setspecs.")

def only_one(list_object):
    """If list_object has exactly 1 item, returns it. Otherwise raises ValueError"""
    if len(list_object) == 1:
        return list_object[0]
    else:
        raise ValueError("Expected a list with exactly one item")

# def get_ait_collection_id(record):
#     if record.header.identifier[:34] ==  'http://archive-it.org/collections/':
#         return int(record.header.identifier[34:])
#     else:
#         eprint(record.header.identifier)
#         raise ValueError("Can't parse collection number.")

# def collection_id_range(records):
#     oids = [ get_ait_collection_id(record) for record in records ]
#     if len(oids) > 1:
#         return (min(oids), max(oids))
#     else:   
#         eprint(oids)
#         raise ValueError("Can't get collection id number range.")

        

class Command(BaseCommand):
    help = 'Crudely imports some data about Archive-It collections'

    def handle(self, *args, **kwargs):
        ait = Sickle(AIT_COLLECTIONS_API)
        records = ait.ListRecords(metadataPrefix='oai_dc')
        for record in records:
            uri2 = record.metadata.pop('identifier')
            uri = models.nocrypto_url( record.header.identifier )

            institution_uri, institution_api = get_organization(record)
            collection = models.Collection.objects.get_or_create(
                archiveit_identifier=uri,
                defaults={
                    'name': "Autogenerated Collection for {}".format(uri),
                    'institution': models.Institution.objects.get_or_create(
                        archiveit_identifier=institution_uri,
                        defaults={
                            'name': "Autogenerated Institution for {}".format(institution_uri)
                        }
                    )[0]
                }
            )[0]


            models.APIEndpoint.objects.get_or_create(
                institution = collection.institution,
                url = institution_api,
                protocol = PROTOCOL,
            )

            metadata_record = collection.metadata_records.get_or_create(
                asserted_by=AGENT,
                metadata_type=MDTYPE,
            )[0]
            metadata_record.metadata = record.raw
            metadata_record.full_clean()
            metadata_record.save()

            try:
                collection.name = ' / '.join( record.metadata.pop('title') )
            except Exception as ex:
                eprint(ex, type(ex))

            # try:
            #     collection.description = only_one(record.metadata.pop('description'))
            # except Exception as ex:
            #     eprint(ex, type(ex), record.metadata.keys())

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

            collection.full_clean()
            collection.save()
