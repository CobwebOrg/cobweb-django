import re
from sys import stdout
from typing import Optional

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel
import reversion
import sickle
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch, NoSetHierarchy

import cobweb.types as T
from core.models import Organization
from core.models import normalize_url, Resource


wayback_url_parser = re.compile(
    r'https?\:\/\/wayback\.archive\-it\.org\/\d+\/\*\/(\w+\:\/\/.*)')

def parse_wayback_url(wayback_url):
    try:
        return normalize_url(wayback_url_parser.match(wayback_url).groups()[0])
    except Exception as ex:
        raise ex


class ImportedRecord(models.Model):

    class Meta:
        unique_together = ('source_feed', 'identifier')

    source_feed = models.ForeignKey('APIEndpoint', on_delete=models.CASCADE)
    identifier = models.CharField(max_length=2000, unique=True)
    record_type = models.CharField(max_length=2000)
    resource = models.ForeignKey('core.Resource', on_delete=models.PROTECT,
                                 null=True, blank=True)
    metadata = JSONField(default={})

    parents = models.ManyToManyField('self', related_name='children',
                                     blank=True, symmetrical=False)

    @property
    def name(self) -> str:
        for name_field in ('title', 'name'):
            try:
                return ' / '.join(self.metadata[name_field])
            except KeyError:
                pass   # try the next name_field!
        return self.identifier
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"""ImportedRecord(
            source_feed=({self.source_feed}),
            identifier=({self.identifier}),
            record_type={self.record_type},
            metadata={self.metadata},
        )
        """

                
@reversion.register()
class APIEndpoint(PolymorphicModel):

    class Meta:
        verbose_name = "API Endpoint"

    organization = models.ForeignKey(Organization, null=True, blank=True,
                                     on_delete=models.SET_NULL)
    url = models.URLField(max_length=200, unique=True)
    last_updated = models.DateTimeField(null=True, editable=False)

    record_type: str = 'resource'
    encoding: Optional[str] = None

    def harvest(self) -> None:
        raise NotImplementedError('APIEndpoint.harvest() needs to be implemented by a subclass.')

    @property
    def name(self):
        return self.url

    def __str__(self):
        return self.url
    
    def __repr__(self):
        return f'<APIEndpoint self.url>'


class OAIPMHEndpoint(APIEndpoint):

    class Meta:
        verbose_name = "OAI-PMH Endpoint"

    set_type: str = 'collection'

    def harvest(self) -> None:
        timestamp = timezone.now()
        sickle = Sickle(self.url, encoding=self.encoding)

        print("Harvesting API Identification")
        print(self.url)
        self.harvest_api_identification(sickle)

        print("Harvesting OAI-PMH Sets as {}".format(self.set_type))
        try:
            for set_info in sickle.ListSets():
                print(set_info.setName[:80], end='\r')
                stdout.flush()
                self.harvest_setspec(set_info)
        except NoSetHierarchy:
            pass

        print("Harvesting OAI-PMH Records as {}".format(self.record_type))
        try:
            for record in sickle.ListRecords(metadataPrefix='oai_dc'):
                print(record.header.identifier[:80], end='\r')
                stdout.flush()
                self.harvest_record(record)
        except NoRecordsMatch:
            pass
        print()
        self.last_updated = timestamp
        self.save()

    def harvest_api_identification(self, sickle: Sickle) -> None:
        metadata = dict(sickle.Identify())

        assert len(metadata['baseURL']) == 1
        assert normalize_url(metadata['baseURL'][0]) == normalize_url(self.url)

    def harvest_setspec(self, set_info) -> None:
        try:
            ImportedRecord.objects.get_or_create(
                identifier=self.get_set_id(set_info.setSpec),
                defaults={'source_feed': self,
                            'metadata': {'title': [set_info.setName]}}
            )
        except ValueError:
            # sometimes a dummy setspec can't be parsed - just ignore!
            pass

    def harvest_record(self, record: sickle.models.Record) -> ImportedRecord:
        record_identifier = normalize_url(record.header.identifier)

        set_identifiers = [self.get_set_id(setspec) 
                           for setspec in record.header.setSpecs]

        try:
            target = ImportedRecord.objects.get(identifier=record_identifier)
        except ImportedRecord.DoesNotExist:
            target = ImportedRecord(identifier=record_identifier)
        target.source_feed = self
        target.record_type = self.record_type
        target.metadata = record.metadata
        target.save()

        for set_id in [self.get_set_id(setspec) for setspec in record.header.setSpecs]:
            target.parents.add(
                ImportedRecord.objects.get_or_create(identifier=set_id)[0] 
            )
        
        return target

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
            )
        except ValueError:
            # sometimes a dummy setspec can't be parsed - just ignore!
            pass

        super().harvest_setspec(set_info)


class AITPartnerEndpoint(BaseAITEndpoint):
    """OAIPMHImporter for individual Archive-it collections."""

    class Meta:
        verbose_name = "Archive-It Partner OAI-PMH Endpoint"

    def harvest_record(self, record: sickle.models.Record) -> ImportedRecord:
        """Harvest a single record for an Archive-It collection."""

        imported_record = super().harvest_record(record)
        imported_record.resource = Resource.objects.get_or_create(
            url=parse_wayback_url(record.header.identifier)
        )[0]
        imported_record.save()
        return imported_record
