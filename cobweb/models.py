from enum import Enum
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
import ipdb



def nocrypto_url(url):
    return( url
        .replace('https://', 'http://')
        .replace('sftp://', 'ftp://')
    )


class NocryptoURLField(models.URLField):
    """Subclass of URLField that maps https to http and sftp to ftp."""
    def clean(self, value, model_instance):
        return super().clean(nocrypto_url(value), model_instance)

class ModelValidationMixin(object):
    """Django currently doesn't force validation on the model level
    for compatibility reasons. We enforce here, that on each save,
    a full valdation run will be done the for model instance"""
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class MetadataType(models.Model):
    name = models.CharField(max_length=200, unique=True, default='unknown')
    identifier = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class MetadataRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object_described = GenericForeignKey('content_type', 'object_id')

    asserted_by = models.ForeignKey('Agent')

    metadata_type = models.ForeignKey(MetadataType)
    metadata = models.TextField()

    def __str__(self):
        return "{}, {}, {}". format(
            self.object_described,
            self.metadata_type,
            self.asserted_by,
        )

# class Tag(models.Model):
#     tag_property = models.TextField(null=False, blank=False, default='tag')
#     tag_value = models.TextField(max_length=200, unique=False)

#     def __str__(self):
#         if self.tag_property:
#             return "{}:{}".format(self.tag_property, self.tag_value)
#         else:
#             return self.tag_value

#     class Meta:
#         unique_together = ("tag_property", "tag_value")

class APIProtocol(models.Model):
    name = models.CharField(max_length=200, unique=True)
    identifier = models.URLField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.name

class APIEndpoint(models.Model):
    location = models.URLField(max_length=200, unique=True)
    institution = models.ForeignKey('Institution')
    protocol = models.ForeignKey(APIProtocol)

    def __str__(self):
        return self.location

class User(AbstractUser):

    description = models.TextField('Description', null=True, blank=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    # metadata_records = GenericRelation(MetadataRecord)
    # tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.get_full_name() or self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

class Software(models.Model):
    name = models.CharField(max_length=200, unique=True)

    description = models.TextField('Description', null=True, blank=True)
    
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    # metadata_records = GenericRelation(MetadataRecord)
    # tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name_plural = "Software"

    def __str__(self):
        return self.name

    @classmethod
    def current_website_software(cls):
        return cls.objects.get_or_create(name="Cobweb Website")[0]

class Agent(models.Model):
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    software = models.ForeignKey(Software, on_delete=models.PROTECT)
    
    class Meta:
        unique_together = ("user", "software")
    
    def __str__(self):
        return ', '.join([str(self.user), str(self.software)])

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_agent(sender, instance, created, **kwargs):
    if created:
        Agent.objects.get_or_create(
            user=instance, 
            software=Software.current_website_software()
        )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_agent(sender, instance, **kwargs):
    Agent.objects.get(user=instance, software=Software.current_website_software()).save()
    
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
    
class Institution(models.Model):
    name = models.CharField('Name', max_length=200, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
        
    address = models.CharField('Address', max_length=1000, null=True, blank=True)
    
    description = models.TextField('Description', null=True, blank=True)

    class SECTORS(Enum):
        academic = ('a', 'Academic')
        corporate = ('c', 'Corporate')
        government = ('g', 'Government')
        nonprofit = ('n', 'Non-Profit')
        other = ('o', 'Other')
    sector = models.CharField('Sector', max_length=1, null=True, blank=True,
        choices = [x.value for x in SECTORS])
        
    class INSTITUTION_TYPES(Enum):
        archive = ('arc', 'Archive')
        datacenter = ('dat', 'Datacenter')
        department = ('dpt', 'Department')
        division = ('div', 'Division')
        laboratory = ('lab', 'Laboratory')
        library = ('lib', 'Library')
        museum = ('mus', 'Museum')
        project = ('pro', 'Project')
        other = ('oth', 'Other')
    institution_type = models.CharField('Type', max_length=3, null=True, blank=True,
        choices=[x.value for x in INSTITUTION_TYPES])
        
    # country = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    metadata_records = GenericRelation(MetadataRecord)
    raw_metadata = models.TextField(null=True, blank=True)
    # tags = models.ManyToManyField(Tag)

    identifier = models.URLField("Archive-It.org Identifier",
        null=True, blank=True, unique=True, editable=False)
           
    def __str__(self):
        return self.name

class InstitutionIdentifier(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    
    class INSTITUTION_IDENTIFIER_TYPES(Enum):
        isni = ('i', 'ISNI')
        ringgold = ('r', 'Ringgold')
        other = ('o', 'Other')
    id_type = models.CharField('Type', max_length=3,
        choices=[x.value for x in INSTITUTION_IDENTIFIER_TYPES])
    
    value = models.CharField('Value', max_length=200)

class Project(models.Model):
    name = models.CharField('Name', max_length=200)
    established_by = models.ForeignKey(Agent, on_delete=models.PROTECT)

    description = models.TextField('Description', null=True, blank=True)
#    keywords ## Separate data type w/ many-to-many relationship??? ##
#    descriptor
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    # metadata_records = GenericRelation(MetadataRecord)
    # tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

class Collection(ModelValidationMixin, models.Model):
    name = models.CharField('Name', max_length=200, unique=False)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, null=True, blank=True)
    
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    metadata_records = GenericRelation(MetadataRecord)
    raw_metadata = models.TextField(null=True, blank=True)
    # tags = models.ManyToManyField(Tag)

    identifier = NocryptoURLField("Archive-It.org Identifier",
        null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.name



class Resource(models.Model):
    root_url = models.URLField()

    nominated_projects = models.ManyToManyField(
        'Project',
        through='Nomination',
        related_name='nominated_resources'
    )
    
    # metadata_records = GenericRelation(MetadataRecord)
    # tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.root_url

class Nomination(models.Model):
    resource = models.ForeignKey(Resource)
    project = models.ForeignKey(Project)
    nominated_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    description = models.TextField('Description', null=True, blank=True)
    # keywords
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    # metadata_records = GenericRelation(MetadataRecord)
    # tags = models.ManyToManyField(Tag)
    
    class Meta:
        unique_together = ('resource', 'project', 'nominated_by')

    def __str__(self):
        return ','.join(map(str, (self.resource, self.project, self.nominated_by)))

class Claim(models.Model):
    resource = models.ForeignKey(Resource)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    # scope = ???
    start_date = models.DateField('Starting Date')
    end_date = models.DateField('Ending Date', null=True, blank=True)
    # frequency = ???
    max_links = models.IntegerField('Maximum Links', null=True, blank=True)
    # host_limit = ???
    time_limit = models.DurationField('Time Limit', null=True, blank=True)
    document_limit = models.IntegerField('Document Limit', null=True, blank=True)
    data_limit = models.IntegerField('Data Limit (GB)', null=True, blank=True) # Allow fractional GB????
    robot_exclusion_override = models.BooleanField('Override Robot Exclusion?', default=False)
    # capture_software = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    # metadata_records = GenericRelation(MetadataRecord)
    # tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return ','.join(map(str, (self.resource, self.collection, self.asserted_by)))

class Holding(models.Model):
    resource = models.ForeignKey(Resource)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    metadata_records = GenericRelation(MetadataRecord)
    raw_metadata = models.TextField(null=True, blank=True)
    # tags = models.ManyToManyField(Tag)
    
    # scope = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    
    def __str__(self):
        return ','.join(map(str, (self.resource, self.collection, self.asserted_by)))
