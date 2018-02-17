import reversion
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse

from cobweb import settings
from metadata.models import CobwebMetadataMixin, Keyword


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

    def __str__(self) -> str:
        """
        Return a string representation of project.

        Should be self.title, but returns 'Project <ID>' if title is blank.
        """
        return self.title or 'Project {}'.format(self.pk)

    def get_absolute_url(self) -> str:
        return reverse('project_detail', kwargs={'pk': self.pk})

    def get_add_nomination_url(self) -> str:
        return reverse('nominate', kwargs={'project_id': self.pk})

    def get_edit_url(self) -> str:
        return reverse('project_update', kwargs={'pk': self.pk})

    def is_admin(self, user: AbstractBaseUser) -> bool:
        return user in self.administrators.all()

    def is_nominator(self, user: AbstractBaseUser) -> bool:
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
class Nomination(models.Model):
    title = models.TextField(null=True, blank=True)
    resource = models.ForeignKey(
        'webresources.Resource',
        on_delete=models.PROTECT,
        related_name='nominations'
    )
    project = models.ForeignKey(Project, related_name='nominations',
                                on_delete=models.PROTECT)

    description = models.TextField('Description', null=True, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)

    # descriptors =
    # language =

    # mutability =

    status = models.CharField(max_length=11, default='Unclaimed', choices=[
        (x, x) for x in ('Rejected', 'Unclaimed', 'Underclaimed', 'Claimed', 'Deprecated')])
    nominated_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    @property
    def name(self) -> str:
        return self.title or self.resource.url

    class Meta:
        unique_together = ('resource', 'project')

    def get_absolute_url(self) -> str:
        return reverse('nomination_detail', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        return reverse('nomination_update', kwargs={'pk': self.pk})

    def get_resource_set(self) -> QuerySet:
        return self.project

    def is_admin(self, user: AbstractBaseUser) -> bool:
        return self.project.is_nominator(user)

    def __str__(self):
        return f'{self.resource} – Project {self.project}'

    def __repr__(self):
        return f'Nomination {self.resource}, project={self.project}'


@reversion.register()
class Claim(models.Model):
    nomination = models.ForeignKey(Nomination, related_name='claims',
                                   on_delete=models.PROTECT)
    collection = models.ForeignKey('archives.Collection', related_name='claims',
                                   on_delete=models.PROTECT)

    description = models.TextField('Description', null=True, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)

    class Meta:
        unique_together = ('nomination', 'collection')

    def __str__(self) -> str:
        return f'{self.nomination} – Collection {self.collection}'

    def get_absolute_url(self) -> str:
        return reverse('claim_detail', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        return reverse('claim_update', kwargs={'pk': self.pk})

    def get_resource_set(self) -> QuerySet:
        return self.nomination.project

    def is_admin(self, user: AbstractBaseUser) -> bool:
        return self.nomination.is_admin(user) or self.collection.is_admin(user)
