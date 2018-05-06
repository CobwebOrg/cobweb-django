import reversion
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse

from cobweb import settings


@reversion.register()
class Project(models.Model):
    """Django ORM model for a Cobweb project."""

    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)

    administrators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects_administered',
        verbose_name='administrators'
    )

    nomination_policy = models.CharField(
        max_length=10, default='Public', choices=(
            ('Public', "Public: anyone can nominate, even if they're not logged in."),
            ('Cobweb Users', 'Cobweb Users: anyone with a Cobweb account can nominate.'),
            ('Restricted', 'Restricted: only selected users and organizations can nominate.'),
        )
    )

    nominator_orgs = models.ManyToManyField(
        'core.Organization', blank=True,
        related_name='projects_nominating',
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

    status = models.CharField(
        max_length=8, default='Active',
        choices=(
            (
                ('Open', 'Open for Nomination'),
                ('Deprecated', "Deprecated (no further nominations recommended)"),
                ('Inactive', 'Inactive (closed to nomination)'),
                ('Deleted', 'Deleted'),
            )
        )
    )

    @property
    def impact_factor(self) -> int:
        # TODO: Fix this stub – not sure I understand the FRs...
        return self.nominations.exclude(claims=None).count()

    @property
    def resources(self) -> models.QuerySet:
        # TODO: this is a bad, inefficient implementation
        return Resource.objects.filter(nomination__project=Self)

    tags = models.ManyToManyField('core.Tag', blank=True)
    subject_headings = models.ManyToManyField('core.SubjectHeading',
                                              blank=True)

    notes = GenericRelation('core.Note')

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
                self.nomination_policy == 'Public'
                or (self.nomination_policy == 'Cobweb Users' and not user.is_anonymous)
                or user in self.administrators.all()
                or user in self.nominators.all()
            )
        )
    
    @property
    def nominations_unclaimed(self) -> QuerySet:
        return self.nominations.filter(claims=None)
    
    @property
    def n_unclaimed(self) -> int:
        return self.nominations_unclaimed.count()
    
    @property
    def nominations_claimed(self) -> QuerySet:
        return self.nominations.exclude(claims=None)  #.filter(holdings=None)
    
    @property
    def n_claimed(self) -> int:
        return self.nominations_claimed.count()
    
    # def nominations_held(self) -> QuerySet:
    #     return self.nominations.exclude(claims=None).exclude(holdings=None)


@reversion.register()
class Nomination(models.Model):
    resource = models.ForeignKey(
        'core.Resource',
        on_delete=models.PROTECT,
        related_name='nominations'
    )
    project = models.ForeignKey(Project, related_name='nominations',
                                on_delete=models.PROTECT)

    # STATUS
    needs_claim = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    nominated_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    rationale = models.TextField(null=True, blank=True)

    suggested_crawl_frequency = models.CharField(
        null=True, blank=True, max_length=50,
        choices=[(x, x) for x in ('Hourly', 'Daily', 'Weekly', 'Monthly')]
    )
    suggested_crawl_end_date = models.DateTimeField(null=True, blank=True)

    notes = GenericRelation('core.Note')

    @property
    def impact_factor(self):
        return self.endorsements.count() + self.claims.count()  # + self.holdings.count()

    @property
    def name(self) -> str:
        return self.title or self.resource.url

    class Meta:
        unique_together = ('resource', 'project')

    def get_absolute_url(self) -> str:
        return reverse('nomination_detail', kwargs={'pk': self.pk})

    def get_claim_url(self) -> str:
        return reverse('claim_create', kwargs={'nomination_pk': self.pk})

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

    organization = models.ForeignKey('core.Organization', related_name='claims',
                                     null=False, blank=False, on_delete=models.PROTECT)

    # STATUS
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    crawl_scope = models.ForeignKey('core.CrawlScope', null=True, blank=True,
                                    on_delete=models.CASCADE)
    notes = GenericRelation('core.Note')

    @property
    def impact_factor(self) -> bool:
        has_holding = [c.holdings.filter(url=self.resource.url).count() > 0
                       for c in self.organization.collections.all()]
        return True in has_holding

    class Meta:
        unique_together = ('nomination', 'organization')

    def __str__(self) -> str:
        return f'{self.nomination} – Organization {self.organization}'

    def get_absolute_url(self) -> str:
        return reverse('claim_detail', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        return reverse('claim_update', kwargs={'pk': self.pk})

    def get_resource_set(self) -> QuerySet:
        return self.nomination.project

    def is_admin(self, user: AbstractBaseUser) -> bool:
        return self.nomination.is_admin(user) or self.organization.is_admin(user)
