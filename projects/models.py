import reversion
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse

from cobweb import settings
from cobweb.models import CobwebModelMixin


@reversion.register()
class Project(CobwebModelMixin, models.Model):
    """Django ORM model for a Cobweb project."""
    
    name_fields = ('title',)

    title = models.CharField(max_length=500, unique=True)
    description = models.TextField(null=True, blank=False)

    administrators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects_administered',
        verbose_name='administrators',
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
    

    tags = models.ManyToManyField('core.Tag', blank=True)
    subject_headings = models.ManyToManyField('core.SubjectHeading',
                                              blank=True)

    notes = GenericRelation('core.Note')

    def get_absolute_url(self) -> str:
        return reverse('project_summary', kwargs={'pk': self.pk})

    def get_add_nomination_url(self) -> str:
        return reverse('project_nominate', kwargs={'project_pk': self.pk})

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
        return self.nominations.annotate(
            n_claims=models.Count('claims', filter=models.Q(claims__has_holding__exact=False))
        ).filter(n_claims__gt=0)

    @property
    def n_claimed(self) -> int:
        return self.nominations_claimed.count()
    
    @property
    def nominations_held(self) -> QuerySet:
        return self.nominations.annotate(
            n_claims=models.Count('claims', filter=models.Q(claims__has_holding__exact=True))
        ).filter(n_claims__gt=0)

    @property
    def n_held(self) -> int:
        return self.nominations_held.count()


@reversion.register()
class Nomination(CobwebModelMixin, models.Model):
    class Meta:
        unique_together = ('resource', 'project')
        
    resource = models.ForeignKey(
        'core.Resource',
        on_delete=models.PROTECT,
        related_name='nominations'
    )
    project = models.ForeignKey(Project, related_name='nominations',
                                on_delete=models.CASCADE)

    # TODO: move to ResourceDescription

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('core.Tag', blank=True)
    subject_headings = models.ManyToManyField('core.SubjectHeading', blank=True)
    language = models.ForeignKey('languages_plus.Language', null=True, blank=True,
                                 on_delete=models.PROTECT)
    # TODO: setup required - see https://github.com/cordery/django-languages-plus
    
    # STATUS
    # needs_claim = models.BooleanField(default=True)
    @property
    def needs_claim(self):
        return self.claims.count() == 0

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
    def impact_factor(self) -> int:
        return (self.endorsements.count() + self.claims.count() +
                self.claims.filter(has_holding=True).count())

    @property
    def name(self) -> str:
        return self.title or self.resource.title or self.resource.url


    def get_absolute_url(self) -> str:
        return reverse('nomination_claims', kwargs={'project_pk': self.project.pk,
                                                    'url': self.resource.url})

    def get_edit_url(self) -> str:
        return reverse('nomination_update', kwargs={
            # 'pk': self.pk,
            'project_pk': self.project.pk,
            'url': self.resource.url,
        })

    def get_claim_url(self) -> str:
        return reverse('claim_create', kwargs={'nomination_pk': self.pk})

    def get_resource_set(self) -> QuerySet:
        return self.project
    
    @property
    def has_holding(self) -> bool:
        return not self.needs_claim and self.claims.filter(has_holding=True).count() > 0

    @property
    def status(self) -> str:
        if self.deleted:
            return 'deleted'
        elif self.needs_claim:
            return 'unclaimed'
        elif not self.has_holding:
            return 'claimed'
        else:
            return 'held'

    def is_admin(self, user: AbstractBaseUser) -> bool:
        return self.project.is_nominator(user)


@reversion.register()
class Claim(CobwebModelMixin, models.Model):
    class Meta:
        unique_together = ('nomination', 'organization')

    nomination = models.ForeignKey(Nomination, related_name='claims',
                                   on_delete=models.CASCADE)

    organization = models.ForeignKey('core.Organization', related_name='claims',
                                     null=False, blank=False, on_delete=models.PROTECT)

    # STATUS
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    has_holding = models.BooleanField(default=False)

    imported_record = models.ForeignKey('webarchives.ImportedRecord', null=True, blank=True,
                                        on_delete=models.SET_NULL, related_name='claims')

    crawl_scope = models.ForeignKey('core.CrawlScope', null=True, blank=True,
                                    on_delete=models.CASCADE)

    notes = GenericRelation('core.Note')

    @property
    def impact_factor(self) -> int:
        if self.has_holding:
            return 2
        else:
            return 1

    def __str__(self) -> str:
        return f'{self.nomination} – Organization {self.organization}'

    def get_absolute_url(self) -> str:
        return reverse('claim_detail', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        return reverse('claim_update', kwargs={'pk': self.pk})

    def make_name(self, exclude=set(), sep='\n'):
        return sep.join((
            nomination.resource.url,
            organization,
            nomination.project,
        ))

    def get_resource_set(self) -> QuerySet:
        return self.nomination.project

    def is_admin(self, user: AbstractBaseUser) -> bool:
        return self.organization.is_admin(user)
