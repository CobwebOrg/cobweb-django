import reversion
from enum import Enum
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField

from projects.models import Project
from webresources.models import NormalizedURLField


@reversion.register()
class User(AbstractUser):

    affiliations = models.ManyToManyField(
        'Organization',
        related_name="affiliated_users"
    )

    description = models.TextField('Description', null=True, blank=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)

    def __str__(self):
        return (
            self.get_full_name() or self.username or 'User {}'.format(self.pk)
        )

    def get_projects_and_collections(self, to_nominate=True):
        # Performance will be awful - gotta re-implement w/ DB query
        return [project for project in Project.objects.all()
                if project.is_nominator(self)]

        # open_noms = Q(nomination_policy__exact='A')
        # if self.is_authenticated():
        #     open_noms = open_noms | Q(nomination_policy__exact='O')
        # restricted_noms = Q(nomination_policy__exact='R')

        # is_admin = Q(administered_by__contains=self)
        # is_nom = Q(nominators__contains=self)
        # not_blacklisted = Q(blacklisted_nominators__notcontains=self)

        # return Project.objects.filter(
        #     is_admin | (
        #         not_blacklisted & (
        #             open_noms
        #             | (restricted_noms & is_nom)
        #         )
        #     )
        # )

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('admin:core_user_change', args=[self.pk])
        # return reverse('', kwargs={'object_id': self.pk})

    def html(self):
        return ("<span class='badge badge-pill badge-info'>{}</span>"
                .format(self))


# @reversion.register()
# class AgentIdentifier(models.Model):
#     agent = models.ForeignKey('Agent', on_delete=models.CASCADE)
#     class AGENT_IDENTIFIER_TYPES(Enum):
#         orcid = ('ORC', 'ORCID')
#         researcherid = ('RID', 'ResearcherID')
#         scopus = ('SCO', 'Scopus')
#         twitter = ('TWI', 'Twitter Handle')
#         other = ('OTH', 'Other')
#     id_type = models.CharField('Type', max_length=3,
#         choices=[x.value for x in AGENT_IDENTIFIER_TYPES])
#     value = models.TextField()


@reversion.register()
class Organization(models.Model):
    name = models.TextField('Name', null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               null=True, blank=True)

    address = models.TextField('Address', null=True, blank=True)

    description = models.TextField('Description', null=True, blank=True)

    metadata = JSONField(null=True, blank=True)
    raw_metadata = models.TextField(null=True, blank=True)

    class SECTORS(Enum):
        academic = ('a', 'Academic')
        corporate = ('c', 'Corporate')
        government = ('g', 'Government')
        nonprofit = ('n', 'Non-Profit')
        other = ('o', 'Other')
    sector = models.CharField('Sector', max_length=1, null=True, blank=True,
                              choices=[x.value for x in SECTORS])

    class ORGANIZATION_TYPES(Enum):
        archive = ('arc', 'Archive')
        datacenter = ('dat', 'Datacenter')
        department = ('dpt', 'Department')
        division = ('div', 'Division')
        laboratory = ('lab', 'Laboratory')
        library = ('lib', 'Library')
        museum = ('mus', 'Museum')
        project = ('pro', 'Project')
        other = ('oth', 'Other')
    organization_type = models.CharField(
        'Type', max_length=3, null=True, blank=True,
        choices=[x.value for x in ORGANIZATION_TYPES]
    )

    # country = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)

    raw_metadata = models.TextField(null=True, blank=True)
    # tags = models.ManyToManyField(Tag)

    identifier = NormalizedURLField(
        "Archive-It.org Identifier",
        null=True, blank=True, unique=True, editable=False
    )

    def __str__(self):
        return (
            self.name or self.identifier or 'Organization {}'.format(self.pk)
        )

# @reversion.register()
# class OrganizationIdentifier(models.Model):
#     organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

#     class ORGANIZATION_IDENTIFIER_TYPES(Enum):
#         isni = ('i', 'ISNI')
#         ringgold = ('r', 'Ringgold')
#         other = ('o', 'Other')
#     id_type = models.CharField('Type', max_length=3,
#         choices=[x.value for x in ORGANIZATION_IDENTIFIER_TYPES])

#     value = models.TextField('Value')
