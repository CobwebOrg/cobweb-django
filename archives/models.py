from django.db import models

from core.models import ModelValidationMixin
from webresources.models import NocryptoURLField



class Collection(ModelValidationMixin, models.Model):
    name = models.CharField('Name', max_length=200, unique=False)
    organization = models.ForeignKey(
    	'core.Organization', on_delete=models.PROTECT, null=True, blank=True)
    
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    metadata = models.ManyToManyField('metadata.Metadatum')
    raw_metadata = models.TextField(null=True, blank=True)

    identifier = NocryptoURLField(null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.name or 'Collection {}'.format(self.pk)

class Claim(models.Model):
    resource = models.ForeignKey('webresources.Resource', on_delete=models.CASCADE)
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
    
    metadata = models.ManyToManyField('metadata.Metadatum')
    def __str__(self):
        return '{} in {}'.format(self.resource, self.collection)

class Holding(models.Model):
    resource = models.ForeignKey('webresources.Resource', on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    
    metadata = models.ManyToManyField('metadata.Metadatum')
    raw_metadata = models.TextField(null=True, blank=True)
    
    # scope = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    
    def __str__(self):
        return '{} in {}'.format(self.resource, self.collection)