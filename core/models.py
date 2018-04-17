import typing

import reversion
from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from itertools import chain
from surt import handyurl
from surt.DefaultIAURLCanonicalizer import canonicalize


validate_url = URLValidator()


def normalize_url(url: str) -> str:
    normalized_url = (
        canonicalize(handyurl.parse(url)).geturl()
        .replace('https://', 'http://')
        .replace('sftp://', 'ftp://')
    )
    validate_url(normalized_url)
    return normalized_url


class NormalizedURLField(models.URLField):
    """Subclass of URLField that maps https to http and sftp to ftp."""

    def clean(self, value, model_instance):
        return super().clean(normalize_url(value), model_instance)


@reversion.register()
class User(AbstractUser):
    # TODO: inherit from ABU??? AU??? use builtin User???

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
        # TODO:
        return reverse('admin:core_user_change', args=[self.pk])
        # return reverse('', kwargs={'object_id': self.pk})


@reversion.register()
class Organization(models.Model):
    name = models.TextField('Name', null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               null=True, blank=True)

    administrators = models.ManyToManyField(
        User, null=True,
        related_name='organizations_administered',
    )

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

    def is_admin(self, user):
        return user in self.administrators.all()


@reversion.register()
class Note(models.Model):
    """A note about an object tracked in Cobweb.

    Fields:
    author : User
        (Null if the original author's account is deleted)
    when_created : DateTime
    ref : GenericForeignKey
    visibility : str / enum
        'Public', 'Organizational', or 'Project'
    text : str
    """

    author = models.ForeignKey(User, null=True, blank=False,
                               on_delete=models.SET_NULL, related_name='notes')
    when_created = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    ref = GenericForeignKey('content_type', 'object_id')

    visibility = models.CharField(max_length=20, default='Public', choices=(
        ('Public', 'Public'),
        ('Organizational', 'Organizational'),
        ('Project', 'Project'),
    ))

    text = models.TextField()


@reversion.register()
class Tag(models.Model):
    """A single tag."""

    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self) -> str:
        """Return tag as string."""
        return self.name


class SubjectHeading(models.Model):
    """A FAST subject heading (cf. https://www.oclc.org/research/themes/data-science/fast.html)."""

    name = models.CharField(max_length=200, unique=True)

    # TODO: Validate based on official list? Pre-load list in migration?

    def __str__(self) -> str:
        return self.name


class Resource(models.Model):
    url = NormalizedURLField(max_length=1000, null=False, blank=False,
                             unique=True)
    notes = GenericRelation(Note)

    def __str__(self) -> str:
        return self.get_url()

    def get_resource_records(self) -> typing.Iterable:
        return chain(
            self.nominations.all(),
            self.tags.all(),
        )

    def get_url(self) -> str:
        return self.url or 'Resource {}'.format(self.pk)

    def get_absolute_url(self) -> str:
        return reverse('core:detail', kwargs={'url': self.url})

    def resource_record_count(self) -> int:
        return (
            self.nominations.count()
            + self.tags.count()
        )


@reversion.register
class ResourceDescription(models.Model):
    """Desecriptive metadata about a Resource, asserted by a User."""

    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)
    asserted_by = models.ForeignKey(User, on_delete=models.PROTECT)

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # TODO: setup required - see https://github.com/cordery/django-languages-plus
    language = models.ForeignKey('languages_plus.Language', null=True, blank=True,
                                 on_delete=models.PROTECT)

    tags = models.ManyToManyField(Tag, blank=True)
    subject_headings = models.ManyToManyField(SubjectHeading, blank=True)


    class Meta:
        unique_together = ('resource', 'asserted_by')

    def __str__(self) -> str:
        return f'{self.resource} asserted_by={self.asserted_by}'


@reversion.register()
class ResourceScan(models.Model):
    """Descriptive metadata about a Resource, retrieved automatically."""

    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)
    when = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Unknown', choices=(
        ('Active', 'Active'),
        ('Redirected', 'Redirected'),
        ('Inactive', 'Inactive'),
        ('Unknown', 'Unknown'),
    ))

    title = models.CharField(max_length=200, null=True, blank=True)
    language = models.ForeignKey('languages_plus.Language', null=True, blank=True,
                                 on_delete=models.PROTECT)
