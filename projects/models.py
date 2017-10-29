import reversion
from enum import Enum
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse

from cobweb import settings
from metadata.models import CobwebMetadataMixin


@reversion.register()
class Project(CobwebMetadataMixin, models.Model):
    name = models.CharField('Name', max_length=500)
    administered_by = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='projects_administered')

    class NOMINATION_POLICY(Enum):
        anonymous = ('A', 'Anonymous')
        open_nom = ('O', 'Open')
        restricted_nom = ('R', 'Restricted')

    nomination_policy = models.CharField(max_length=1, default='o',
        choices = [x.value for x in NOMINATION_POLICY])

    nominators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
        related_name='projects_nominating')

    nominator_blacklist = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        blank=True, related_name='projects_blacklisted')

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
    
    def get_add_nomination_url(self):
        return reverse('nominate', kwargs={'project_id': self.pk})

    def get_edit_url(self):
        return reverse('project_update', kwargs={'pk': self.pk})

    def is_admin(self, user):
        return user in self.administered_by.all()

    def is_nominator(self, user):
        return ( 
            user not in self.nominator_blacklist.all()
            and (
                self.nomination_policy == 'A' 
                or (self.nomination_policy == 'O' and not user.is_anonymous())
                or user in self.administered_by.all() 
                or user in self.nominators.all() 
            )
        )

@reversion.register()
class Nomination(CobwebMetadataMixin, models.Model):
    resource = models.ForeignKey('webresources.Resource', 
        on_delete=models.PROTECT, related_name='nominations')
    project = models.ForeignKey(Project)
    nominated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT)
    
    class Meta:
        unique_together = ('resource', 'project', 'nominated_by')

    def get_resource_set(self):
        return self.project

    def is_admin(self, user):
        return self.project.is_nominator(user)

    def __str__(self):
        return '{resource} nominated by {agent} in {project}'.format(
            resource = self.resource,
            project = self.project,
            agent = self.nominated_by
        )