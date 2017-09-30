import reversion
from enum import Enum
from django.db import models
from django.urls import reverse

from cobweb import settings



@reversion.register()
class Project(models.Model):
    name = models.TextField('Name')
    administered_by = models.ManyToManyField(settings.AUTH_USER_MODEL)

    description = models.TextField('Description', null=True, blank=True)
    metadata = models.ManyToManyField('metadata.metadatum')
    # keywords = models.ManyToManyField('metadata.Keyword')

    class STATUS(Enum):
        active = ('a', 'Active')
        inactive = ('i', 'Inactive')
        deleted = ('d', 'Deleted')
    status = models.CharField(max_length=1, default='a',
        choices = [x.value for x in STATUS])
    
    def __str__(self):
        return self.name or 'Project {}'.format(self.pk)
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

@reversion.register()
class Nomination(models.Model):
    resource = models.ForeignKey('webresources.Resource')
    project = models.ForeignKey(Project)
    nominated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT)
    
    description = models.TextField('Description', null=True, blank=True)
    # keywords
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    class Meta:
        unique_together = ('resource', 'project', 'nominated_by')

    def __str__(self):
        return '{resource} nominated by {agent} in {project}'.format(
            resource = self.resource,
            project = self.project,
            agent = self.nominated_by
        )