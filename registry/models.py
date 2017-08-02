from django.db import models
from django.urls import reverse


    
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
   
class Agent(models.Model):
    # type = ???
    name = models.CharField('Name', max_length=200)
    description = models.TextField('Description', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    # identifier = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    affiliation = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

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
        return reverse('registry:project_detail', kwargs={'pk': self.pk})

class Seed(models.Model):
    url = models.URLField()
    description = models.TextField('Description', null=True, blank=True)
    # keywords
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    project_set = models.ManyToManyField(Project)
    nominated_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.url

class Claim(models.Model):
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
    
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    def __str__(self):
        return '{} claims {}'.format(self.institution, self.seed)

class Holding(models.Model):
    # scope = ???
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    asserted_by = models.ForeignKey(Agent, on_delete=models.PROTECT)
    
    def __str__(self):
        return '{} has {}'.format(self.institution, self.seed)
