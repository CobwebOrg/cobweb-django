import reversion
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField

from webresources.models import NormalizedURLField


@reversion.register()
class User(AbstractUser):

    affiliations = models.ManyToManyField(
        'Organization',
        related_name="affiliated_users"
    )

    description = models.TextField('Description', null=True, blank=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)

    def __str__(self) -> str:
        return (
            self.get_full_name() or self.username or 'User {}'.format(self.pk)
        )

    def get_absolute_url(self) -> str:
        return reverse('user_detail', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        return reverse('admin:core_user_change', args=[self.pk])
        # return reverse('', kwargs={'object_id': self.pk})


@reversion.register()
class Organization(models.Model):
    name = models.TextField('Name', null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               null=True, blank=True)

    address = models.TextField('Address', null=True, blank=True)

    description = models.TextField('Description', null=True, blank=True)

    metadata = JSONField(null=True, blank=True)

    SECTORS = ('Academic', 'Corporate', 'Government', 'Non-Profit', 'Other')
    sector = models.CharField('Sector', max_length=10, null=True, blank=True,
                              choices=[(x, x) for x in SECTORS])

    ORGANIZATION_TYPES = ('Archive', 'Datacenter', 'Department', 'Division',
                          'Laboratory', 'Library', 'Museum', 'Project', 'Other')
    organization_type = models.CharField(
        'Type', max_length=10, null=True, blank=True,
        choices=[(x, x) for x in ORGANIZATION_TYPES]
    )

    # country = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)

    identifier = NormalizedURLField(
        "Archive-It.org Identifier",
        null=True, blank=True, unique=True, editable=False
    )

    def __str__(self) -> str:
        return (
            self.name or self.identifier or 'Organization {}'.format(self.pk)
        )



@reversion.register()
class Tag(models.Model):
    """A single tag."""

    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self) -> str:
        """Return tag as string."""
        return self.name
