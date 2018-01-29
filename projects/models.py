import reversion
from django.db import models
from django.urls import reverse

from cobweb import settings
from metadata.models import CobwebMetadataMixin


@reversion.register()
class Project(CobwebMetadataMixin, models.Model):
    """Django ORM model for a Cobweb project."""

    administrators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects_administered',
        verbose_name='administrators'
    )

    nomination_policy = models.CharField(
        max_length=10, default='Open', choices=(
            ('Anonymous', "Anonymous: anyone can nominate, even if they're not logged in."),
            ('Open', 'Open: anyone with a Cobweb account can nominate.'),
            ('Restricted', 'Restricted: only selected users can nominate.'),
        )
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

    STATUS = ('Active', 'Inactive', 'Deleted')
    status = models.CharField(
        max_length=8, default='Active',
        choices=[(x, x) for x in STATUS]
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

    def is_admin(self, user):
        return user in self.administrators.all()

    def is_nominator(self, user):
        return (
            user not in self.nominator_blacklist.all()
            and (
                self.nomination_policy == 'Anonymous'
                or (self.nomination_policy == 'Open' and not user.is_anonymous)
                or user in self.administrators.all()
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
    project = models.ForeignKey(Project, related_name='nominations',
                                on_delete=models.PROTECT)

    nominated_by = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = ('resource', 'project')

    def get_absolute_url(self):
        return reverse('nomination_detail', kwargs={'pk': self.pk})

    def get_resource_set(self):
        return self.project

    def is_admin(self, user):
        return self.project.is_nominator(user)

    def __str__(self):
        return f'{self.resource} – Project {self.project}'

    def __repr__(self):
        return f'Nomination {self.resource}, project={self.project}'


@reversion.register()
class Claim(CobwebMetadataMixin, models.Model):

    title = models.TextField(null=True, blank=True)

    nomination = models.ForeignKey(Nomination, related_name='claims',
                                   on_delete=models.PROTECT)
    collection = models.ForeignKey('archives.Collection', related_name='claims',
                                   on_delete=models.PROTECT)

    class Meta:
       unique_together = ('nomination', 'collection')

    # NOTE: the Cobweb data model documentation includes a large number of
    # fields related to capture software parameters. I plan on storing them in
    # the 'metadata' JSONField that Claim inherits from CobwebMetadataMixin.
    # For the full list, see projects.views.ClaimCreateView.get_initial()
    # TODO: some sort of schema / validation system...

    def __str__(self):
        return f'{self.nomination} – Collection {self.collection}'

    def get_absolute_url(self):
        return reverse('claim_update', kwargs={'pk': self.pk})

    def get_resource_set(self):
        return self.collection
