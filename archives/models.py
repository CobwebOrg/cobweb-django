import reversion
from django.db import models
from django.urls import reverse

from metadata.models import CobwebMetadataMixin
from webresources.models import NormalizedURLField


class ModelValidationMixin(object):
    """Django currently doesn't force validation on the model level
    for compatibility reasons. We enforce here, that on each save,
    a full valdation run will be done the for model instance"""
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Collection(ModelValidationMixin, CobwebMetadataMixin, models.Model):
    name = models.TextField('Name', unique=False)
    organization = models.ForeignKey(
        'core.Organization', null=True, blank=True,
        on_delete=models.PROTECT, related_name='collections'
    )

    identifier = NormalizedURLField(null=True, blank=True, unique=True)

    def get_absolute_url(self):
        return reverse('admin:archives_collection_change', args=[self.pk])
        # return reverse('collection_detail', kwargs={'object_id': self.pk})

    def __str__(self):
        return self.name or 'Collection {}'.format(self.pk)


@reversion.register()
class Claim(CobwebMetadataMixin, models.Model):
    resource = models.ForeignKey(
        'webresources.Resource',
        on_delete=models.PROTECT,
        related_name='claims'
    )
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    # scope = ???
    start_date = models.DateField('Starting Date')
    end_date = models.DateField('Ending Date', null=True, blank=True)
    # frequency = ???
    max_links = models.IntegerField('Maximum Links', null=True, blank=True)
    # host_limit = ???
    time_limit = models.DurationField('Time Limit', null=True, blank=True)
    document_limit = models.IntegerField('Document Limit',
                                         null=True, blank=True)
    data_limit = models.IntegerField('Data Limit (GB)', null=True, blank=True)
    robot_exclusion_override = models.BooleanField('Override Robot Exclusion?',
                                                   default=False)
    # capture_software = ???

    def __str__(self):
        return '{} in {}'.format(self.resource, self.collection)

    def get_resource_set(self):
        return self.collection


@reversion.register()
class Holding(CobwebMetadataMixin, models.Model):
    resource = models.ForeignKey(
        'webresources.Resource',
        on_delete=models.PROTECT,
        related_name='holdings'
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='holdings'
    )

    # scope = ???

    def __str__(self):
        return '{} in {}'.format(self.resource, self.collection)

    def get_resource_set(self):
        return self.collection
