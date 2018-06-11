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

import cobweb.types as typ
from cobweb.models import CobwebModelMixin


def normalize_url(url: typ.URL) -> typ.NormalizedURL:
    normalized_url = (
        canonicalize(handyurl.parse(url)).geturl()
        .replace('https://', 'http://')
        .replace('sftp://', 'ftp://')
    )
    return normalized_url


class NormalizedURLField(models.URLField):
    """Subclass of URLField that maps https to http and sftp to ftp."""

    def clean(self, value, model_instance):
        return super().clean(normalize_url(value), model_instance)


@reversion.register()
class User(CobwebModelMixin, AbstractUser):
    name_fields = ('username',)

    first_name = models.CharField(max_length=200, null=True, blank=False)
    last_name = models.CharField(max_length=200, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)

    organization = models.ForeignKey('Organization', null=True, blank=True,
                                     related_name="affiliated_users",
                                     on_delete=models.SET_NULL)
    professional_title = models.CharField(max_length=200, null=True, blank=True)

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

    @property
    def name(self):
        full_name = self.get_full_name()
        return self.username + (f'\n{full_name}' if full_name else '')

    def __str__(self) -> str:
        return self.get_full_name() or self.username or 'User {}'.format(self.pk)

    def can_claim(self, organization=None) -> bool:
        if organization:
            return self.organization == organization
        else:
            return self.organization is not None

    def get_absolute_url(self) -> str:
        return reverse('user_detail', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        # TODO:
        return reverse('admin:core_user_change', args=[self.pk])
        # return reverse('', kwargs={'object_id': self.pk})


@reversion.register()
class Organization(CobwebModelMixin, models.Model):

    full_name = models.CharField(max_length=2000, unique=True,
                                 verbose_name="full legal name")
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

    contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                blank=True, related_name="contact_for")

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
        return self.claims.count() + self.claims.filter(has_holding=True).count()

    def __repr__(self) -> str:
        return f"<Organization '{self.name}'>"

    def __str__(self) -> str:
        return (
            self.name or self.identifier or 'Organization {}'.format(self.pk)
        )
    
    def get_absolute_url(self):
        return reverse('organization_detail', kwargs={'pk': self.pk})

    def is_admin(self, user):
        return user in self.administrators.all()


@reversion.register()
class Note(CobwebModelMixin, models.Model):
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

    @property
    def name(self) -> str:
        if hasattr(self, '_name'):
            return self._name
        else:
            return '\n'.join((
                self.author,
                self.when_created,
                're: ' + self.ref,
            ))


@reversion.register()
class Tag(CobwebModelMixin, models.Model):
    """A single tag."""
    name_fields = ('title',)
    title = models.CharField(max_length=200, unique=True, db_index=True)


class SubjectHeading(CobwebModelMixin, models.Model):
    """A FAST subject heading (cf. https://www.oclc.org/research/themes/data-science/fast.html)."""
    name_fields = ('title',)
    title = models.CharField(max_length=200, unique=True)

    # TODO: Validate based on official list? Pre-load list in migration?


class Resource(CobwebModelMixin, models.Model):
    name_fields = ('url',)

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

    def get_resource_records(self) -> typ.Iterable:
        return chain(
            self.nominations.all(),
        )

    def get_absolute_url(self) -> str:
        return reverse('resource_detail', kwargs={'url': self.url})

    def resource_record_count(self) -> int:
        return (
            self.nominations.count()
        )


@reversion.register
class ResourceDescription(CobwebModelMixin, models.Model):
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
class CrawlScope(CobwebModelMixin, models.Model):
    class Meta:
        unique_together = ('title', 'organization')

    title = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

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
