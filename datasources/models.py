import inspect, re, reversion
from sys import stderr, stdout

import os

# from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from sickle import Sickle

from archives.models import Collection, Holding
from core.models import Organization
from webresources.models import normalize_url, NormalizedURLField, Resource

# from datasources.importers import importers


@reversion.register()
class APIEndpoint(models.Model):
    location = models.URLField(max_length=200, unique=True)
    organization = models.ForeignKey('core.Organization', 
            null=True, blank=True)

    importer_class_name = models.TextField( default = 'OAIPMHImporter',
            # choices = [(name, name) for name in importers.keys()],
            choices = [(x,x) for x in
                 ('AITCollectionsImporter', 'AITPartnerImporter')]
        )

    last_updated = models.DateTimeField(null=True, editable=False)

    metadata = JSONField(null=True, blank=True)
    raw_metadata = models.TextField(null=True, blank=True)

    @classmethod
    def get_archiveit_root(cls,):
        return cls.objects.get_or_create(
            location = 'https://archive-it.org/oai',
            defaults = {
                'importer_class_name': 'AITCollectionsImporter',
                'organization': Organization
                    .objects.get_or_create(
                        identifier='http://archive-it.org/',
                        defaults={'name': "Archive-It.org"}
                    )[0],
            }
        )[0]

    def get_importer(self):
        return importers[self.importer_class_name](self)

    def harvest(self):
        self.get_importer().harvest()
        self.last_updated = timezone.now()

    def __str__(self):
        return self.location or 'APIEndpoint {}'.format(self.pk)

def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

# def get_organization(record):
#     if (len(record.header.setSpecs) == 1 
#             and record.header.setSpecs[0][:13] == 'organization:'):
#         id_number = record.header.setSpecs[0][13:] # actually should be string
#         org_url, api_url = setspec_to_urls(only_one(setspec))
#         return uri, api_url
#     else:
#         eprint(record.header.identifier, record.header.setSpecs)
#         raise ValueError('Can't find organization from setspecs.')

def only_one(list_object):
    """If list_object has only 1 item, return it. Otherwise raise ValueError"""
    if len(list_object) == 1:
        return list_object[0]
    else:
        eprint(list_object)
        raise ValueError('Expected a list with exactly one item')

class Importer:
    IS_IMPORTER = True

    def harvest(self):
        with reversion.create_revision():
            reversion.set_user(get_user_model().objects.get_or_create(
                username="admin")[0])
            reversion.set_comment("Imported from: {}".format(repr(self.api)))
            self.__harvest_all__()

    def __str__(self):
        return str(self.api)

class OAIPMHImporter(Importer):
    set_class = Collection
    record_class = Holding
    set_key = 'collection'
    record_key = 'resource'

    def __init__(self, api):
        self.api = api
        self.sickle = Sickle(self.api.location)

    def __harvest_all__(self):
        print("Harvesting API Identification")
        print(self.api.location)
        self.__harvest_api_identification__()

        try:
            print("Harvesting OAI-PMH Sets as {}".format(self.set_class))
            for setspec in self.sickle.ListSets():
                try:
                    print('{:<50}'.format(setspec.setName), end='\r')
                    stdout.flush()
                except:
                    pass
                self.__harvest_setspec__(setspec)
        except Exception as ex:
            eprint("In {}.__harvest_all__()".format(self))
            eprint(ex, type(ex))

        try:
            print("Harvesting OAI-PMH Records as {}".format(self.record_class))
            for record in self.sickle.ListRecords(metadataPrefix='oai_dc'):
                try:
                    print('{:<50}'.format(record.header.identifier), end='\r')
                    stdout.flush()
                except:
                    pass
                self.__harvest_record__(record)
        except Exception as ex:
            eprint("In {}.__harvest_all__()".format(self))
            eprint(ex, type(ex))


    def __harvest_record__(self, record):
        uri = normalize_url( record.header.identifier )

        set_uri = self.__get_set_identifier__(only_one(record.header.setSpecs))

        target = self.record_class.objects.get_or_create(
            identifier=uri,
            defaults={
                'name': 'Autogenerated {} for {}'
                    .format(self.record_class, uri),
                self.set_key: self.set_class.objects.get_or_create(
                    identifier=set_uri,
                    defaults={
                        'name': 'Autogenerated {} for {}'
                        .format(self.set_class, set_uri)
                    }
                )[0]
            }
        )[0]

        target.raw_metadata = record.raw

        try:
            target.name = ' / '.join( record.metadata['title'] )
        except Exception as ex:
            eprint("In {}.__harvest_record__({})".format(
                self, record.header.identifier))
            eprint(ex, type(ex))

        # try:
        #     target.description = '\n'.join(record.metadata['description'])
        # except Exception as ex:
        #     eprint(ex, type(ex))

        target.raw_metadata = record.raw
        self.__attach_metadata__(target, record.metadata, 'oai_dc')
        target.save()


    def __get_set_identifier__(self, setspec):
        return setspec

    def __harvest_api_identification__(self):
        api = APIEndpoint.objects.get(location=self.api.location)
        api_identify = self.sickle.Identify()
        metadata = dict(api_identify)

        assert ( normalize_url( only_one( metadata.pop('baseURL') )) 
            == normalize_url(self.api.location) )

        if api.organization:
            api.organization.name = only_one(metadata['repositoryName'])
            api.organization.save()

        api.raw_metadata = api_identify.raw
        self.__attach_metadata__(api, metadata, 'DC?')
        api.save()

    def __harvest_setspec__(self, source):
        try:
            uri = self.__get_set_identifier__(source.setSpec)
            if uri:
                target = self.set_class.objects.get_or_create(identifier=uri)[0]
                target.name = source.setName
                target.save()
            else:
                # can't get a valid set identifier
                pass
        except Exception as ex:
            eprint("In {}.__harvest_setspec__({})".format(self, source))
            eprint(ex, type(ex))

    def __attach_metadata__(self, target, metadata, vocabulary_name):
        record_md = []
        for key, values in metadata.items():
            record_md.extend([
                {
                    'vocabulary': vocabulary_name,
                    'element': key,
                    'value': value
                } for value in values
            ])
        target.metadata = record_md
        target.save()

class AITCollectionsImporter(OAIPMHImporter):
    set_class = Organization
    record_class = Collection
    set_key = 'organization'
    record_key = 'identifier'


    def __harvest_record__(self, record):
        super().__harvest_record__(record)

        for setspec in record.header.setSpecs:
            aitpartner_api = APIEndpoint.objects.get_or_create(
                location = self.__get_set_api__(setspec)
            )[0]
            aitpartner_api.importer_class_name = 'AITPartnerImporter'
            aitpartner_api.organization = Organization.objects.get_or_create(
                identifier = self.__get_set_identifier__(setspec)
            )[0]
            aitpartner_api.save()

    def __get_set_identifier__(self, setspec):
        try:
            set_type, set_number = setspec.split(':')
            return 'http://archive-it.org/{}/{}'.format(
                set_type, set_number)
        except ValueError:
            return None
        except Exception as ex:
            eprint("In {}.__get_set_identifier__:".format(self))
            eprint("setspec = {}".format(setspec))
            eprint(ex, type(ex))

    def __get_set_api__(self, setspec):
        try:
            set_type, set_number = setspec.split(':')
            if set_type == 'organization':
                return ( 'https://archive-it.org/oai/organizations/{}'
                    .format(set_number) )
            else:
                return None
        except Exception as ex:
            eprint("In {}.__get_set_api__({})".format(self, setspec))
            eprint("setspec = {}".format(setspec))
            eprint(ex, type(ex))


class AITPartnerImporter(OAIPMHImporter):
    set_class = Collection
    record_class = Holding
    set_key = 'collection'
    record_key = 'resource'


    def __harvest_record__(self, record):
        root_url = self.__parse_wayback_url__(record.header.identifier)
                
        collection_uri = self.__get_set_identifier__(
            only_one(record.header.setSpecs))

        collection = Collection.objects.get_or_create(
            identifier=collection_uri,
            defaults={
                'name': "Autogenerated Collection for {}"
                        .format(collection_uri),
                'organization': self.api.organization,
            }
        )[0]

        try:
            resource = Resource.objects.get_or_create(
                url=normalize_url(root_url))[0]
        except Exception as e:
            e.args += ( "url = {}".format(normalize_url(root_url)), )
            e.args += "len(url) = {}".format(len(normalize_url(root_url))),
            raise e

        holding = Holding.objects.get_or_create(
            resource=resource,
            collection=collection,
        )[0]

        holding.raw_metadata = record.raw
        self.__attach_metadata__(holding, record.metadata, 'oai_dc')

    def __harvest_setspec__(self, source):
        try:
            uri = self.__get_set_identifier__(source.setSpec)
            if uri:
                target = self.set_class.objects.get_or_create(identifier=uri)[0]
                target.name = source.setName
                target.save()
            else:
                # can't get a valid set identifier
                pass
        except Exception as ex:
            eprint("In {}.__harvest_setspec__({})".format(self, source))
            eprint(ex, type(ex))

    def __get_set_identifier__(self, setspec):
        try:
            set_type, set_number = setspec.split(':')
            return 'http://archive-it.org/organizations/{}'.format(
                set_type, set_number)
        except ValueError:
            return None
        except Exception as ex:
            eprint("In {}.__get_set_identifier__:".format(self))
            eprint("setspec = {}".format(setspec))
            eprint(ex, type(ex))

    def __parse_wayback_url__(self, wayback_url):
        wayback_url_parser = re.compile(
            'http\:\/\/wayback\.archive\-it\.org\/\d+\/\*/(https?\:\/\/.*)')

        return normalize_url( 
            wayback_url_parser
            .match(wayback_url)
            .groups()[0]
        )

importers = { name: thing for name, thing in globals().items()
              if inspect.isclass(thing) and issubclass(thing, Importer) }
