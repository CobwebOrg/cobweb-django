import reversion
from django.contrib.auth import get_user_model
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
    administrators = models.ManyToManyField(get_user_model(), related_name='collections_administered')
    invited_administrators = models.ManyToManyField(get_user_model(), related_name='collections_administered_invited')

    organization = models.ForeignKey(
        'core.Organization', null=True, blank=True,
        on_delete=models.PROTECT, related_name='collections'
    )

    identifier = NormalizedURLField(null=True, blank=True, unique=True)

    def get_absolute_url(self):
        return reverse('archives:collection_detail', kwargs={'pk': self.pk})

    def is_admin(self, user):
        return user in self.administrators.all()

    def __str__(self):
        return self.title or 'Collection {}'.format(self.pk)


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
