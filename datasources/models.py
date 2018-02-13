import collections
import inspect
import re
from sys import stderr, stdout

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import FieldError
from django.db import models
from django.utils import timezone
import reversion
from sickle import Sickle

from archives.models import Collection, Holding
from core.models import Organization
from webresources.models import normalize_url, Resource

# from datasources.importers import importers


@reversion.register()
class APIEndpoint(models.Model):

    class Meta:
        verbose_name = "API Endpoint"

    location = models.URLField(max_length=200, unique=True)
    organization = models.ForeignKey('core.Organization', null=True,
                                     blank=True, on_delete=models.CASCADE,)

    importer_class_name = models.TextField( default = 'OAIPMHImporter',
            choices = [(x,x) for x in
                 ('AITCollectionsImporter', 'AITPartnerImporter')]
        )

    last_updated = models.DateTimeField(null=True, editable=False)

    metadata = JSONField(null=True, blank=True)

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
        update_start_time = timezone.now()
        self.get_importer().harvest()
        self.last_updated = update_start_time
        self.save()

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
            self.harvest_all()

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

    def harvest_all(self):
        print("Harvesting API Identification")
        print(self.api.location)
        self.harvest_api_identification()

        print("Harvesting OAI-PMH Sets as {}".format(self.set_class))
        for setspec in self.sickle.ListSets():
            print(setspec.setName[:80], end='\r')
            stdout.flush()
            self.harvest_setspec(setspec)

        print("Harvesting OAI-PMH Records as {}".format(self.record_class))
        for record in self.sickle.ListRecords(metadataPrefix='oai_dc'):
            print(record.header.identifier[:80], end='\r')
            stdout.flush()
            self.harvest_record(record)
        print()

    def harvest_record(self, record):
        uri = normalize_url(record.header.identifier)

        set_uri = self.get_set_identifier(only_one(record.header.setSpecs))

        target = self.record_class.objects.get_or_create(
            identifier=uri,
            defaults={
                'title': 'Autogenerated {} for {}'
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

        try:
            target.title = ' / '.join(record.metadata.pop('title'))
        except KeyError:
            pass  # no 'title' in record.metadata; that's fine!

        try:
            target.description = '\n\n'.join(record.metadata.pop('description'))
        except KeyError:
            pass  # no 'description' in record.metadata; that's fine!

        self.attach_metadata(target, record.metadata, 'oai_dc')
        target.save()


    def get_set_identifier(self, setspec):
        return setspec

    def harvest_api_identification(self):
        api = APIEndpoint.objects.get(location=self.api.location)
        api_identify = self.sickle.Identify()
        metadata = dict(api_identify)

        assert (normalize_url(only_one(metadata.pop('baseURL')))
                == normalize_url(self.api.location))

        # For Archive-it it's always
        # "Archive-It Web Partner Url Seed Collections"
        # if api.organization:
        #     api.organization.title = only_one(metadata['repositoryName'])
        #     api.organization.save()

        self.attach_metadata(api, metadata, 'DC?')
        api.save()

    def harvest_setspec(self, source):
        try:
            uri = self.get_set_identifier(source.setSpec)
            if uri:
                target = self.set_class.objects.get_or_create(identifier=uri)[0]
                target.title = source.setName
                target.save()
            else:
                # can't get a valid set identifier
                pass
        except Exception as ex:
            eprint("In {}.harvest_setspec({})".format(self, source))
            eprint(ex, type(ex))

    def attach_metadata(self, target, metadata, vocabulary_name):
        record_md = collections.defaultdict(list)
        for key, values in metadata.items():
            record_md[key].extend(values)
        target.metadata = record_md
        target.save()


class AITCollectionsImporter(OAIPMHImporter):
    """OAIPMHImporter for Archive-It's master list of collections."""

    set_class = Organization
    record_class = Collection
    set_key = 'organization'
    record_key = 'identifier'

    def harvest_record(self, record):
        """Harvest a single record for an Archive-It collection."""
        super().harvest_record(record)

        for setspec in record.header.setSpecs:
            aitpartner_api = APIEndpoint.objects.get_or_create(
                location=self.get_set_api(setspec)
            )[0]
            aitpartner_api.importer_class_name = 'AITPartnerImporter'
            aitpartner_api.organization = Organization.objects.get_or_create(
                identifier=self.get_set_identifier(setspec)
            )[0]
            aitpartner_api.save()

    def get_set_identifier(self, setspec):
        """Convert a setspec to a url-type identifier."""
        try:
            set_type, set_number = setspec.split(':')
            return 'http://archive-it.org/{}s/{}'.format(
                set_type, set_number)
        except ValueError:
            return None
        except Exception as ex:
            eprint("In {}.get_set_identifier__:".format(self))
            eprint("setspec = {}".format(setspec))
            eprint(ex, type(ex))

    def get_set_api(self, setspec):
        """Infer API Enpoint from setspec."""
        try:
            set_type, set_number = setspec.split(':')
            if set_type == 'organization':
                return ('https://archive-it.org/oai/organizations/{}'
                        .format(set_number))
            else:
                return None
        except Exception as ex:
            eprint("In {}.get_set_api({})".format(self, setspec))
            eprint("setspec = {}".format(setspec))
            eprint(ex, type(ex))


class AITPartnerImporter(OAIPMHImporter):
    """OAIPMHImporter for individual Archive-it collections."""

    set_class = Collection
    record_class = Holding
    set_key = 'collection'
    record_key = 'resource'

    def harvest_record(self, record):
        """Harvest a single record for an Archive-It collection."""

        root_url = self.parse_wayback_url(record.header.identifier)

        collection_uri = self.get_set_identifier(
            only_one(record.header.setSpecs))

        collection = Collection.objects.get_or_create(
            identifier=collection_uri,
            defaults={
                'title': "Autogenerated Collection for {}"
                        .format(collection_uri),
                'organization': self.api.organization,
            }
        )[0]

        try:
            resource = Resource.objects.get_or_create(
                url=normalize_url(root_url))[0]
        except Exception as e:
            e.args += ("url = {}".format(normalize_url(root_url)),)
            e.args += "len(url) = {}".format(len(normalize_url(root_url))),
            raise e

        holding = Holding.objects.get_or_create(
            resource=resource,
            collection=collection,
        )[0]

        try:
            holding.title = ' / '.join(record.metadata.pop('title'))
        except KeyError:
            pass  # no 'title' in record.metadata; that's fine!

        try:
            holding.description = '\n\n'.join(record.metadata.pop('description'))
        except KeyError:
            pass  # no 'description' in record.metadata; that's fine!



        self.attach_metadata(holding, record.metadata, 'oai_dc')

    def harvest_setspec(self, source):
        try:
            uri = self.get_set_identifier(source.setSpec)
            if uri:
                target = self.set_class.objects.get_or_create(identifier=uri)[0]
                target.title = source.setName
                target.save()
            else:
                # can't get a valid set identifier, but that's okay
                # usually this is just a dummy record at the start of the list
                pass
        except Exception as ex:
            eprint("In {}.harvest_setspec({})".format(self, source))
            eprint(ex, type(ex))

    def get_set_identifier(self, setspec):
        try:
            set_type, set_number = setspec.split(':')

            return 'http://archive-it.org/{}s/{}'.format(
                set_type, set_number)
        except ValueError:
            return None
        except Exception as ex:
            eprint("In {}.get_set_identifier__:".format(self))
            eprint("setspec = {}".format(setspec))
            eprint(ex, type(ex))

    def parse_wayback_url(self, wayback_url):
        wayback_url_parser = re.compile(
            'http\:\/\/wayback\.archive\-it\.org\/\d+\/\*/(https?\:\/\/.*)')

        return normalize_url(
            wayback_url_parser
            .match(wayback_url)
            .groups()[0]
        )


importers = {name: thing for name, thing in globals().items()
             if inspect.isclass(thing) and issubclass(thing, Importer)}
