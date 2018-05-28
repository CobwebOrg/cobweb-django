import typing

import reversion
from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from itertools import chain
from phonenumber_field.modelfields import PhoneNumberField
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

    first_name = models.CharField(max_length=200, null=True, blank=False)
    last_name = models.CharField(max_length=200, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)

    affiliations = models.ManyToManyField('Organization', blank=True, through='Affiliation',
                                          related_name="affiliated_users")
    # professional_title TODO

    url = NormalizedURLField(null=True, blank=True)

    # Preferences
    get_notification_emails = models.BooleanField(default=True)

    notes = GenericRelation('Note')

    # @property
    # def projects(self):
    #     return 

    @property
    def impact_factor(self):
        # TODO: actuall implement functional requirement
        # (this is just a placeholder)
        return self.projects_administered.count()

    def __repr__(self) -> str:
        return f'User(username="{self.username}")'

    def __str__(self) -> str:
        return self.get_full_name() or self.username or 'User {}'.format(self.pk)

    def can_claim(self, organization=None):
        if organization:
            return organization in user.affiliations
        else:
            return self.affiliations.count() > 0

    def get_absolute_url(self) -> str:
        return reverse('user_detail', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        # TODO:
        return reverse('admin:core_user_change', args=[self.pk])
        # return reverse('', kwargs={'object_id': self.pk})


@reversion.register()
class Organization(models.Model):

    full_name = models.CharField(max_length=2000, verbose_name="full legal name")
    short_name = models.CharField(max_length=200, null=True, blank=True,
                                  verbose_name="short name, nickname, or acronym")

    administrators = models.ManyToManyField(
        User,
        related_name='organizations_administered',
    )

    address = models.TextField(null=True, blank=True)
    telephone_number = PhoneNumberField(null=True, blank=True)
    url = NormalizedURLField(null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)

    contact = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    parent_organization = models.ForeignKey('self', on_delete=models.SET_NULL,
                                            null=True, blank=True)

    description = models.TextField(
        null=True, blank=True,
        verbose_name='description of mission and collecting policy',
    )

    identifier = NormalizedURLField(
        "Archive-It.org Identifier",
        null=True, blank=True, unique=True, editable=False
    )

    @property
    def name(self):
        return self.short_name or self.full_name

    @property
    def impact_factor(self):
        # TODO: actuall implement functional requirement
        # (this is just a placeholder)
        return self.claims.count() + self.holdings.count()

    def __repr__(self) -> str:
        return f"<Organization '{self.name}'>"

    def __str__(self) -> str:
        return (
            self.name or self.identifier or 'Organization {}'.format(self.pk)
        )

    def is_admin(self, user):
        return user in self.administrators.all()


@reversion.register()
class Affiliation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    professional_title = models.CharField(max_length=200, null=True, blank=True)

@reversion.register()
class Note(models.Model):
    """A note about an object tracked in Cobweb.

    Fields:
    author : User
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
        # ('Organizational', 'Organizational'),
        ('Project Members', 'Project Members'),
        ('Project Admins', 'Project Administrators'),
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

    when_checked = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Unknown', choices=(
        ('Active', 'Active'),
        ('Redirected', 'Redirected'),
        ('Inactive', 'Inactive'),
        ('Unknown', 'Unknown'),
    ))

    title = models.CharField(max_length=200, null=True, blank=True)
    language = models.ForeignKey('languages_plus.Language', null=True, blank=True,
                                 on_delete=models.PROTECT)

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
        return reverse('resource_detail', kwargs={'url': self.url})

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


@reversion.register
class CrawlScope(models.Model):
    max_time = models.PositiveIntegerField(null=True, blank=True)
    max_size = models.PositiveIntegerField(null=True, blank=True)
    max_resources = models.PositiveIntegerField(null=True, blank=True)

    override_robot_exclusion = models.NullBooleanField(null=True, blank=True, default=False)

    boundary_behavior = models.CharField(max_length=200, null=True, blank=True,
                                         choices=(
                                            ('Page', 'Page'),
                                            ('Site', 'Site'),
                                            ('Host', 'Host'),
                                            ('Domain', 'Domain'),
                                         ))

    max_embedded_links = models.PositiveIntegerField(null=True, blank=True)
    max_content_links = models.PositiveIntegerField(null=True, blank=True)

    format_behavior = models.CharField(
        max_length=200, null=True, blank=True, default='All', choices=(
            ('All', 'All'),
            ('PDF-Only', 'PDF-Only'),
        )
    )

    technology = models.CharField(
        max_length=200, null=True, blank=True,
        choices=[(x, x) for x in ('Archive-It', 'Brozzler', 'Crawler4j', 'Crawljax',
                                  'Heritrix', 'HTTrack', 'NetarchiveSuite', 'Nutch',
                                  'Social Feed Manager', 'WebRecorder', 'Wget', 'Other',
                                  'Unknown')],
        default='Unknown',
    )
