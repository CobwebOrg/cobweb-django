import collections
import inspect
import re
from sys import stderr, stdout
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import FieldError
from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel
import reversion
from sickle import Sickle

from cobweb.models import CobwebModelMixin
from core.models import Organization
from core.models import normalize_url, Resource


class ImportedRecord(CobwebModelMixin, models.Model):

    class Meta:
        unique_together = ('source_feed', 'identifier')

    name_fields = ('source_feed', 'identifier')

    source_feed = models.ForeignKey('APIEndpoint', on_delete=models.CASCADE)
    identifier = models.CharField(max_length=200)
    record_type = models.CharField(max_length=200)
    metadata = JSONField()

    parents = models.ManyToManyField('self', related_name='children',
                                     blank=True, symmetrical=False)

    @property
    def name(self) -> str:
        for name_field in ('title', 'name'):
            try:
                return ' / '.join(self.metadata[name_field])
            except KeyError:
                pass   # try the next name_field!
        return 'ImportedRecord {self.pk}'
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"""ImportedRecord(
            identifiers=({self.identifiers}),
            record_type={self.record_type},
            metadata={self.metadata},
        )
        """

                
@reversion.register()
class APIEndpoint(CobwebModelMixin, PolymorphicModel):

    class Meta:
        verbose_name = "API Endpoint"
    name_fields = ('url', 'organization')

    organization = models.ForeignKey(Organization, null=True, blank=True,
                                     on_delete=models.SET_NULL)
    url = models.URLField(max_length=200, unique=True)
    last_updated = models.DateTimeField(null=True, editable=False)

    record_type: str = 'resource'
    encoding: Optional[str] = None

    def harvest(self) -> None:
        raise NotImplementedError('APIEndpoint.harvest() needs to be implemented by a subclass.')


class OAIPMHEndpoint(APIEndpoint):

    class Meta:
        verbose_name = "OAI-PMH Endpoint"

    set_type: str = 'collection'

    def harvest(self) -> None:
        sickle = Sickle(self.url, encoding=self.encoding)

        print("Harvesting API Identification")
        print(self.url)
        self.harvest_api_identification(sickle)

        print("Harvesting OAI-PMH Sets as {}".format(self.set_type))
        for set_info in sickle.ListSets():
            print(set_info.setName[:80], end='\r')
            stdout.flush()
            self.harvest_setspec(set_info)

        print("Harvesting OAI-PMH Records as {}".format(self.record_type))
        for record in sickle.ListRecords(metadataPrefix='oai_dc'):
            print(record.header.identifier[:80], end='\r')
            stdout.flush()
            self.harvest_record(record)
        print()

    def harvest_api_identification(self, sickle: Sickle) -> None:
        metadata = dict(sickle.Identify())

        assert len(metadata['baseURL']) == 1
        assert normalize_url(metadata['baseURL'][0]) == normalize_url(self.url)

    def harvest_setspec(self, set_info) -> None:
        try:
            set_id = self.get_set_id(set_info.setSpec)
            if set_id:
                target = ImportedRecord.objects.get_or_create(
                    source_feed=self,
                    identifier=set_id,
                    defaults={'metadata': {'title': [set_info.setName]}}
                )[0]
        except ValueError:
            # sometimes a dummy setspec can't be parsed - just ignore!
            pass

    def harvest_record(self, record) -> None:
        record_identifier = normalize_url(record.header.identifier)

        set_identifiers = [self.get_set_id(setspec) 
                           for setspec in record.header.setSpecs]

        target = ImportedRecord.objects.get_or_create(
            source_feed=self,
            identifier=record_identifier,
            record_type=self.record_type,
            metadata=record.metadata,
        )[0]

        for set_id in [self.get_set_id(setspec) for setspec in record.header.setSpecs]:
            target.parents.add(
                ImportedRecord.objects.get_or_create(identifier=set_id)[0] 
            )

    def get_set_id(self, setspec) -> str:
        return setspec


class BaseAITEndpoint(OAIPMHEndpoint):

    encoding = 'utf-8'

    def get_set_id(self, setspec):
        """Convert a setspec to a url-type identifier."""
        set_type, set_number = setspec.split(':')
        return f'http://archive-it.org/{set_type}s/{set_number}'


class AITCollectionsEndpoint(BaseAITEndpoint):
    """OAIPMHEndpoint for Archive-It's master list of collections."""

    class Meta:
        verbose_name = "Archive-It Master OAI-PMH Endpoint"

    set_type = 'organization'
    record_type = 'collection'


    def harvest_setspec(self, set_info) -> None:
        """Make sure APIEndpoint exists for AIT partner organization."""

        try:
            set_type, set_number = set_info.setSpec.split(':')
            AITPartnerEndpoint.objects.get_or_create(
                url=f'https://archive-it.org/oai/{set_type}s/{set_number}',
            )[0]
        except ValueError:
            # sometimes a dummy setspec can't be parsed - just ignore!
            pass

        super().harvest_setspec(set_info)


class AITPartnerEndpoint(BaseAITEndpoint):
    """OAIPMHImporter for individual Archive-it collections."""

    class Meta:
        verbose_name = "Archive-It Partner OAI-PMH Endpoint"

    def harvest_record(self, record):
        """Harvest a single record for an Archive-It collection."""

        resource = Resource.objects.get_or_create(
            url=self.parse_wayback_url(record.header.identifier)
        )

        super().harvest_record(record, res)

        collection_ids = [self.get_set_id(s) for s in record.header.setSpecs]

        try:
            resource = Resource.objects.get_or_create(
                url=normalize_url(root_url))[0]
        except Exception as e:
            e.args += ("url = {}".format(normalize_url(root_url)),)
            e.args += "len(url) = {}".format(len(normalize_url(root_url))),
            raise e

        # TODO: remove Holding
        # holding = Holding.objects.get_or_create(
        #     resource=resource,
        #     collection=collection,
        # )[0]

        # try:
        #     holding.title = ' / '.join(record.metadata.pop('title'))
        # except KeyError:
        #     pass  # no 'title' in record.metadata; that's fine!

        # try:
        #     holding.description = '\n\n'.join(record.metadata.pop('description'))
        # except KeyError:
        #     pass  # no 'description' in record.metadata; that's fine!



        # self.attach_metadata(holding, record.metadata, 'oai_dc')


    def parse_wayback_url(self, wayback_url):
        wayback_url_parser = re.compile(
            'http\:\/\/wayback\.archive\-it\.org\/\d+\/\*/(https?\:\/\/.*)')

        return normalize_url(
            wayback_url_parser
            .match(wayback_url)
            .groups()[0]
        )