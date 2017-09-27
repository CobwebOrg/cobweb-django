from enum import Enum
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

from webresources.models import NocryptoURLField


class ModelValidationMixin(object):
    """Django currently doesn't force validation on the model level
    for compatibility reasons. We enforce here, that on each save,
    a full valdation run will be done the for model instance"""
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class User(AbstractUser):

    affiliations = models.ManyToManyField('Organization', related_name="affiliated_users")

    description = models.TextField('Description', null=True, blank=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    def __str__(self):
        return self.get_full_name() or self.username or 'User {}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_agent(sender, instance, created, **kwargs):
#     if created:
#         Agent.objects.get_or_create(agent=instance)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_agent(sender, instance, **kwargs):
#     Agent.objects.get(agent=instance).save()
    
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
#     value = models.CharField('Value', max_length=200)
    
class Organization(models.Model):
    name = models.CharField('Name', max_length=200, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
        
    address = models.CharField('Address', max_length=1000, null=True, blank=True)
    
    description = models.TextField('Description', null=True, blank=True)

    metadata = models.ManyToManyField('metadata.Metadatum')

    class SECTORS(Enum):
        academic = ('a', 'Academic')
        corporate = ('c', 'Corporate')
        government = ('g', 'Government')
        nonprofit = ('n', 'Non-Profit')
        other = ('o', 'Other')
    sector = models.CharField('Sector', max_length=1, null=True, blank=True,
        choices = [x.value for x in SECTORS])
        
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
    organization_type = models.CharField('Type', max_length=3, null=True, 
        blank=True, choices=[x.value for x in ORGANIZATION_TYPES])
        
    # country = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    raw_metadata = models.TextField(null=True, blank=True)
    # tags = models.ManyToManyField(Tag)

    identifier = NocryptoURLField("Archive-It.org Identifier",
        null=True, blank=True, unique=True, editable=False)
           
    def __str__(self):
        return self.name or self.identifier or 'Organization {}'.format(self.pk)

# class OrganizationIdentifier(models.Model):
#     organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    
#     class ORGANIZATION_IDENTIFIER_TYPES(Enum):
#         isni = ('i', 'ISNI')
#         ringgold = ('r', 'Ringgold')
#         other = ('o', 'Other')
#     id_type = models.CharField('Type', max_length=3,
#         choices=[x.value for x in ORGANIZATION_IDENTIFIER_TYPES])
    
#     value = models.CharField('Value', max_length=200)
