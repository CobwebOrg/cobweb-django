from django.db import models
from django.urls import reverse
from django.contrib import auth
from django.db.models.signals import post_save
from django.dispatch import receiver


   
class Agent(models.Model):
    # type = ???
    name = models.CharField('Name', max_length=200)
    
    user = models.OneToOneField(auth.models.User, on_delete=models.CASCADE)
    
    description = models.TextField('Description', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    # identifier = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    affiliation = models.ForeignKey('Institution', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=auth.models.User)
def create_user_agent(sender, instance, created, **kwargs):
    if created:
        Agent.objects.create(user=instance)

@receiver(post_save, sender=auth.models.User)
def save_user_agent(sender, instance, **kwargs):
    instance.agent.save()

# class AgentMD(models.Model):
#     describes = models.ForeignKey(Agent)
#     asserted_by = models.ForeignKey(Agent)
#
#     class Meta:
#         unique_together = ("describes", "asserted_by")
    
class Institution(models.Model):
    name = models.CharField('Name', max_length=200)
    description = models.TextField('Description', null=True, blank=True)
    # sector = ???
    # type = ???
    address = models.CharField('Address', max_length=1000, null=True, blank=True)
    # country = ???
    # identifier = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

class InstitutionMD(models.Model):
    describes = models.ForeignKey(Institution)
    asserted_by = models.ForeignKey(Agent)
    
    class Meta:
        unique_together = ("describes", "asserted_by")

class Project(models.Model):
    name = models.CharField('Name', max_length=200)
    description = models.TextField('Description', null=True, blank=True)
#    keywords ## Separate data type w/ many-to-many relationship??? ##
#    descriptor
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)

    established_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

class ProjectMD(models.Model):
    describes = models.ForeignKey(Project, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("describes", "asserted_by")

class Collection(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

class CollectionMD(models.Model):
    describes = models.ForeignKey(Collection, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("describes", "asserted_by")

class Resource(models.Model):
    root_url = models.URLField()

class ResourceMD(models.Model):
    describes = models.ForeignKey(Resource, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("describes", "asserted_by")

class Nomination(models.Model):
    resource = models.ForeignKey(Resource)
    description = models.TextField('Description', null=True, blank=True)
    # keywords
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    project = models.ForeignKey(Project)
    nominated_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    def __str__(self):
        return ','.join(self.resource, self.collection)

# class NominationMD(models.Model):
#     describes = models.ForeignKey(Nomination)
#     asserted_by = models.ForeignKey(Agent)
#
#     class Meta:
#         unique_together = ("describes", "asserted_by")

class Claim(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    
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
    
    asserted_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    def __str__(self):
        return ','.join(self.resource, self.collection)

class ClaimMD(models.Model):
    describes = models.ForeignKey(Claim, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("describes", "asserted_by")

class Holding(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    
    # scope = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    asserted_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    def __str__(self):
        return ','.join(self.resource, self.collection)

class HoldingMD(models.Model):
    describes = models.ForeignKey(Holding, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("describes", "asserted_by")
