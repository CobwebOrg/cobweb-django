"""Miscelaneous Cobweb models. Could be a few apps, but why bother..."""

from collections.abc import Iterable
from itertools import chain
from typing import Dict, List, NewType

import reversion
from django.db import models
from django.forms.models import model_to_dict
from django.urls import reverse
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from phonenumber_field.modelfields import PhoneNumberField
from surt import handyurl
from surt.DefaultIAURLCanonicalizer import canonicalize

import cobweb.types as typ
import help_text


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
class User(AbstractUser):
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

    terms_accepted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    notes = GenericRelation('Note')

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

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def can_claim(self, organization=None) -> bool:
        if organization:
            return self.organization == organization
        else:
            return self.organization is not None

    def get_absolute_url(self) -> str:
        return reverse('user', kwargs={'username': self.username})

    def get_edit_url(self) -> str:
        return self.get_absolute_url()


@reversion.register()
class Organization(models.Model):

    slug = models.SlugField(max_length=50, null=False, unique=True,
                            help_text=help_text.ORGANIZATION_PROFILE)

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return self.short_name or self.full_name

    @property
    def impact_factor(self):
        # TODO: actuall implement functional requirement
        # (this is just a placeholder)
        return self.claims.count() + self.claims.filter(has_holding=True).count()

    @cached_property
    def claims_held(self):
        return self.claims.filter(has_holding=True)

    @cached_property
    def claims_claimed(self):
        return self.claims.filter(has_holding=False)

    @property
    def n_held(self):
        return self.claims_held.count()

    @property
    def n_claimed(self):
        return self.claims_claimed.count()

    def __repr__(self) -> str:
        return f"<Organization '{self.name}'>"

    def __str__(self) -> str:
        return (
            self.name or self.identifier or 'Organization {}'.format(self.pk)
        )

    def get_absolute_url(self):
        return reverse('organization', args=(self.slug,))

    def is_admin(self, user):
        return user in self.administrators.all()


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

    @property
    def name(self) -> str:
        return '\n'.join((
            self.author,
            self.when_created,
            're: ' + self.ref,
        ))


@reversion.register()
class Tag(models.Model):
    """A single tag."""
    title = models.CharField(max_length=200, unique=True, db_index=True)

    @property
    def name(self):
        return self.title

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return f'Tag(title="{self.title}")'


class SubjectHeading(models.Model):
    """A FAST subject heading (cf. https://www.oclc.org/research/themes/data-science/fast.html)."""
    name_fields = ('title',)
    title = models.CharField(max_length=200, unique=True)

    # TODO: Validate based on official list? Pre-load list in migration?

    @property
    def name(self):
        return self.title

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'SubjectHeading(title="{self.title}")'


MDDict = NewType('MDDict', Dict[str, List[str]])
MultiMDDict = NewType('MultiMDDict', Dict[str, MDDict])


class Resource(models.Model):
    # surt = 
    url = NormalizedURLField(max_length=1000, null=False, blank=False,
                             unique=True)

    # METADATA RETRIEVED DIRECTLY FROM SITE

    on_date = models.DateTimeField(null=True, blank=True)

    # Status: Replaced the enum from the spec w/ the following
    is_active = models.NullBooleanField(null=True, blank=True)
    redirect_url = models.URLField(null=True, blank=True)
    # STATUS        is_active       redirect_url
    # Unknown:      Null            Null
    # Active:       True            Null
    # Inactive:     False           Null
    # Redirected:   False           [URL]  # TODO: what should is_active be? does it matter?

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)  # crosswalk to <meta name="keywords">
    creator = models.CharField(max_length=200, null=True, blank=True)
    language = models.ForeignKey('languages_plus.Language', null=True, blank=True,
                                 on_delete=models.PROTECT)

    notes = GenericRelation(Note)

    def __repr__(self):
        return f'Resource(url="{self.url}")'

    def __str__(self):
        return self.url

    def get_resource_records(self) -> typ.Iterable:
        return chain(
            self.nominations.all(),
            self.imported_records.all(),
        )

    def get_absolute_url(self) -> str:
        return reverse('resource', kwargs={'url': self.url})
    
    @property
    def has_metadata(self) -> bool:
        for nomination in self.nominations.all():
            for field in ['title', 'creator', 'language', 'description']:
                value = getattr(nomination, field)
                if value and value != '':
                    return True
            for field in ['tags', 'subject_headings']:
                if getattr(nomination, field).count() > 0:
                    return True

        for imported_record in self.imported_records.all():
            for value_list in imported_record.metadata.values():
                if len(value_list) > 0:
                    return True
        
        return False

    @property
    def name(self):
        return str(self)

    def resource_record_count(self) -> int:
        return self.nominations.count() + self.imported_records.count()


@reversion.register
class CrawlScope(models.Model):
    class Meta:
        unique_together = ('title', 'organization')

    title = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    max_time = models.PositiveIntegerField(null=True, blank=True)
    max_size = models.PositiveIntegerField(null=True, blank=True)
    max_resources = models.PositiveIntegerField(null=True, blank=True)

    override_robot_exclusion = models.NullBooleanField(null=True, blank=True, default=False)

    boundary_behavior = models.CharField(max_length=200, null=True, blank=True,
                                         choices=(('Page', 'Page'),
                                                  ('Site', 'Site'),
                                                  ('Host', 'Host'),
                                                  ('Domain', 'Domain')))

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

    @property
    def name(self):
        return self.title

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return f'CrawlScope(title="{self.title}")'
