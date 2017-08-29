from enum import Enum
from django.db import models
from django.urls import reverse
from django.contrib import auth
from django.db.models.signals import post_save
from django.dispatch import receiver



class Agent(models.Model):
    name = models.CharField('Name', max_length=200)
    
    class AGENT_TYPES(Enum):
        auto = ('a', 'Automated')
        person = ('p', 'Person')
    agent_type = models.CharField('Type', max_length=3,
        choices = [x.value for x in AGENT_TYPES])
        
    user = models.OneToOneField(auth.models.User, on_delete=models.CASCADE, null=True, blank=True)
    
    description = models.TextField('Description', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    affiliation = models.ForeignKey('Institution', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=auth.models.User)
def create_user_agent(sender, instance, created, **kwargs):
    if created:
        Agent.objects.create(user=instance, agent_type=Agent.AGENT_TYPES.person.value[0])

@receiver(post_save, sender=auth.models.User)
def save_user_agent(sender, instance, **kwargs):
    instance.agent.save()
    
class AgentIdentifier(models.Model):
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE)
    class AGENT_IDENTIFIER_TYPES(Enum):
        orcid = ('ORC', 'ORCID')
        researcherid = ('RID', 'ResearcherID')
        scopus = ('SCO', 'Scopus')
        twitter = ('TWI', 'Twitter Handle')
        other = ('OTH', 'Other')
    id_type = models.CharField('Type', max_length=3,
        choices=[x.value for x in AGENT_IDENTIFIER_TYPES])
    value = models.CharField('Value', max_length=200)
    
class Institution(models.Model):
    name = models.CharField('Name', max_length=200)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
        
    address = models.CharField('Address', max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.name

class InstitutionMD(models.Model):
    describes = models.ForeignKey(Institution)
    asserted_by = models.ForeignKey(Agent)
    
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
    
    class Meta:
        unique_together = ("describes", "asserted_by")
           
    def __str__(self):
        return ','.join(map(str, (self.describes, self.asserted_by)))

class InstitutionIdentifier(models.Model):
    institution = models.ForeignKey(InstitutionMD, on_delete=models.CASCADE)
    
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

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

class Collection(models.Model):
    name = models.CharField('Name', max_length=200)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Resource(models.Model):
    root_url = models.URLField()
    
    def __str__(self):
        return self.root_url

# class ResourceMD(models.Model):
#     describes = models.ForeignKey(Resource, on_delete=models.CASCADE)
#     asserted_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ("describes", "asserted_by")
#
#     def __str__(self):
#         return ','.join(map(str, (self.describes, self.asserted_by)))

class Nomination(models.Model):
    resource = models.ForeignKey(Resource)
    project = models.ForeignKey(Project)
    nominated_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    description = models.TextField('Description', null=True, blank=True)
    # keywords
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    def __str__(self):
        return ','.join(map(str, (self.resource, self.project, self.nominated_by)))

# class NominationMD(models.Model):
#     describes = models.ForeignKey(Nomination)
#     asserted_by = models.ForeignKey(Agent)
#
#     class Meta:
#         unique_together = ("describes", "asserted_by")

class Claim(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
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
    
    def __str__(self):
        return ','.join(map(str, (self.resource, self.collection)))

# class ClaimMD(models.Model):
#     describes = models.ForeignKey(Claim, on_delete=models.CASCADE)
#     asserted_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ("describes", "asserted_by")
#     def __str__(self):
#         return ','.join(map(str, (self.describes, self.asserted_by)))

class Holding(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    # scope = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    
    def __str__(self):
        return ','.join(map(str, (self.resource, self.collection)))

class HoldingMD(models.Model):
    describes = models.ForeignKey(Holding, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("describes", "asserted_by")
    
    def __str__(self):
        return ','.join(map(str, (self.describes, self.asserted_by)))