from django.db import models
from django.urls import reverse





class Project(models.Model):
    name = models.CharField('Name', max_length=200)
    established_by = models.ForeignKey('core.Agent', on_delete=models.PROTECT)

    description = models.TextField('Description', null=True, blank=True)
#    keywords ## Separate data type w/ many-to-many relationship??? ##
#    descriptor
    created = models.DateTimeField('Date Created', auto_now_add=True)
    deprecated = models.DateTimeField('Date Deprecated', null=True, blank=True)
    
    def __str__(self):
        return self.name or 'Project {}'.format(self.pk)
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

class Nomination(models.Model):
    resource = models.ForeignKey('webresources.Resource')
    project = models.ForeignKey(Project)
    nominated_by = models.ForeignKey('core.Agent', on_delete=models.PROTECT)
    
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