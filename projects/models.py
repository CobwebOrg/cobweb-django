import reversion
from django.db import models
from django.urls import reverse

from cobweb import settings
from metadata.models import CobwebMetadataMixin


@reversion.register()
class Project(CobwebMetadataMixin, models.Model):
    """Django ORM model for a Cobweb project."""

    administered_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects_administered',
        verbose_name='administrators'
    )

    NOMINATION_POLICY = {
        'A': "Anonymous: anyone can nominate, even if they're not logged in.",
        'O': 'Open: anyone with a Cobweb account can nominate.',
        'R': 'Restricted: only selected users can nominate.',
    }
    nomination_policy = models.CharField(
        max_length=1, default='O',
        choices=[(key, value) for key, value in NOMINATION_POLICY.items()]
    )

    nominators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True,
        related_name='projects_nominating',
    )

    nominator_blacklist = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='projects_blacklisted',
    )

    STATUS = {
        'a': 'Active',
        'i': 'Inactive',
        'd': 'Deleted',
    }
    status = models.CharField(
        max_length=1, default='a',
        choices=[(key, value) for key, value in STATUS.items()]
    )

    def some_nominations(self):
        return self.nominations.all().order_by('-id')[:20]

    def __str__(self):
        """
        Return a string representation of project.

        Should be self.title, but returns 'Project <ID>' if title is blank.
        """
        return self.title or 'Project {}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

    def get_add_nomination_url(self):
        return reverse('nominate', kwargs={'project_id': self.pk})

    def get_edit_url(self):
        return reverse('project_update', kwargs={'pk': self.pk})

    def get_nomination_policy(self):
        return self.NOMINATION_POLICY[self.nomination_policy]

    def get_status(self):
        return self.STATUS[self.status]

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
    resource = models.ForeignKey(
        'webresources.Resource',
        on_delete=models.PROTECT,
        related_name='nominations'
    )
    project = models.ForeignKey(Project, related_name='nominations')
    nominated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    class Meta:
        unique_together = ('resource', 'project', 'nominated_by')

    def get_resource_set(self):
        return self.project

    def is_admin(self, user):
        return self.project.is_nominator(user)

    def __str__(self):
        return '{resource} nominated by {agent} in {project}'.format(
            resource=self.resource,
            project=self.project,
            agent=self.nominated_by,
        )
