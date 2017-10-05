import reversion
from django.db import models
from django.contrib.postgres.fields import JSONField

from webresources.models import NocryptoURLField





class ModelValidationMixin(object):
    """Django currently doesn't force validation on the model level
    for compatibility reasons. We enforce here, that on each save,
    a full valdation run will be done the for model instance"""
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Collection(ModelValidationMixin, models.Model):
    name = models.TextField('Name', unique=False)
    organization = models.ForeignKey(
    	'core.Organization', on_delete=models.PROTECT, null=True, blank=True)
    
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    metadata = JSONField(null=True, blank=True)
    raw_metadata = models.TextField(null=True, blank=True)

    identifier = NocryptoURLField(null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.name or 'Collection {}'.format(self.pk)

@reversion.register()
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
    
    metadata = JSONField(null=True, blank=True)
    def __str__(self):
        return '{} in {}'.format(self.resource, self.collection)

@reversion.register()
class Holding(models.Model):
    resource = models.ForeignKey('webresources.Resource', on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    
    metadata = JSONField(null=True, blank=True)
    raw_metadata = models.TextField(null=True, blank=True)
    
    # scope = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    
    def __str__(self):
        return '{} in {}'.format(self.resource, self.collection)