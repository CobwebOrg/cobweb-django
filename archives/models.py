import reversion
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.urls import reverse

from metadata.models import CobwebMetadataMixin
from webresources.models import NormalizedURLField


class ModelValidationMixin(object):
    """Django currently doesn't force validation on the model level
    for compatibility reasons. We enforce here, that on each save,
    a full valdation run will be done the for model instance"""

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class Collection(ModelValidationMixin, CobwebMetadataMixin, models.Model):
    title = models.TextField(null=True, blank=True)

    administrators = models.ManyToManyField(
        get_user_model(), blank=True,
        related_name='collections_administered',
    )

    organization = models.ForeignKey(
        'core.Organization', null=True, blank=True,
        on_delete=models.PROTECT, related_name='collections'
    )

    identifier = NormalizedURLField(null=True, blank=True, unique=True)

    def get_absolute_url(self) -> str:
        """Return the detail url for collection."""
        return reverse('archives:collection_detail', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        """Return the edit url for collection."""
        return reverse('archives:collection_update', kwargs={'pk': self.pk})

    def is_admin(self, user: AbstractBaseUser) -> bool:
        """Check whether *user* is in collection.administrators."""
        return user.is_authenticated and (
            user in self.administrators.all()
            or self.administrators.all().count() == 0
        )

    def __str__(self) -> str:
        """Get user-readable string representation of collection."""
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

    def __str__(self) -> str:
        return f'{self.resource} in {self.collection}'

    def get_resource_set(self) -> Collection:
        """Return the Collection containing a Holding."""
        return self.collection
