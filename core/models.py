from itertools import chain
from collections import Counter, defaultdict
from typing import Dict, List, Union

import reversion
from django.core.validators import URLValidator
from django.db import models
from django.forms.models import model_to_dict
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from phonenumber_field.modelfields import PhoneNumberField
from surt import handyurl
from surt.DefaultIAURLCanonicalizer import canonicalize

import cobweb.types as typ


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

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def can_claim(self, organization=None) -> bool:
        return True
        # if organization:
        #     return self.organization == organization
        # else:
        #     return self.organization is not None

    def get_absolute_url(self) -> str:
        return reverse('user_detail', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        # TODO:
        return reverse('admin:core_user_change', args=[self.pk])
        # return reverse('', kwargs={'object_id': self.pk})


@reversion.register()
class Organization(models.Model):

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
        return f'<Tag self.title>'


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
        return f'<SubjectHeading self.title>'


class Resource(models.Model):
    # surt = 
    url = NormalizedURLField(max_length=1000, null=False, blank=False,
                             unique=True)

    notes = GenericRelation(Note)

    def __repr__(self):
        return f'<Resource {self.url}>'

    def __str__(self):
        return self.url

    @property
    def data(self) -> Dict[str, List[str]]:
        data: Dict[str, Counter] = defaultdict(Counter)
        
        data['url'][self.url] = 1
        for source in chain(self.resource_scans.all(), self.resource_descriptions.all()):  # pylint: disable=E1101
            for field, values in source.data.items():
                for value in values:
                    data[field][value] += 1

        for unwanted_field in ('id', 'asserted_by'):
            try:
                del data[unwanted_field]
            except KeyError:
                pass
        ans = {}

        for field, values_counter in data.items():
            ans[field] = [value for value, n in values_counter.most_common()]

        return ans

    def get_resource_records(self) -> typ.Iterable:
        return chain(
            self.nominations.all(),
        )

    def get_absolute_url(self) -> str:
        return reverse('resource_detail', kwargs={'url': self.url})

    @property
    def name(self):
        for source in chain(self.resource_scans.all(), self.resource_descriptions.all()):
            if source.title:
                return source.title
        return self.url

    def resource_record_count(self) -> int:
        return (
            self.nominations.count()
        )


@reversion.register
class ResourceScan(models.Model):
    """Resource Metadata automatically retrieved by crawling the URL."""

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, unique=True,
                                 related_name='resource_scans')
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
    author = models.CharField(max_length=200, null=True, blank=True)
    language = models.ForeignKey('languages_plus.Language', null=True, blank=True,
                                 on_delete=models.PROTECT)

    @property
    def data(self) -> Dict[str, List[str]]:
        return {k: (v if isinstance(v, list) else [v])
                for k, v in model_to_dict(self).items()}

    def __repr__(self) -> str:
        return f'<ResourceScan {self.resource} on_date={self.on_date}>'

@reversion.register
class ResourceDescription(models.Model):
    """Desecriptive metadata about a Resource, asserted by a User."""

    class Meta:
        unique_together = ('resource', 'asserted_by')

    resource = models.ForeignKey(Resource, on_delete=models.PROTECT,
                                 related_name='resource_descriptions')
    asserted_by = models.ForeignKey(User, on_delete=models.PROTECT)

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)

    # TODO: setup required - see https://github.com/cordery/django-languages-plus
    language = models.ForeignKey('languages_plus.Language', null=True, blank=True,
                                 on_delete=models.PROTECT)

    tags = models.ManyToManyField(Tag, blank=True)
    subject_headings = models.ManyToManyField(SubjectHeading, blank=True)

    @property
    def data(self) -> Dict[str, List[str]]:
        return {k: (v if isinstance(v, list) else [v])
                for k, v in model_to_dict(self).items()}

    def __repr__(self) -> str:
        return f'<ResourceDescription {self.resource} asserted_by={self.asserted_by}>'


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
        return f'<CrawlScope self.title>'
