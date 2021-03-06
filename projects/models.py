import reversion
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse

import help_text
from cobweb import settings


@reversion.register()
class Project(models.Model):
    """Django ORM model for a Cobweb project."""

    slug = models.SlugField(max_length=50, null=False, unique=True,
                            help_text=help_text.PROJECT_SLUG)

    title = models.CharField(max_length=500, unique=True)
    description = models.TextField(null=True, blank=False,
                                   help_text=help_text.PROJECT_DESCRIPTION)
    collecting_scope = models.TextField(
        null=True, blank=True,
        help_text=help_text.PROJECT_COLLECTING_SCOPE,
        )

    administrators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects_administered',
        verbose_name='administrators',
        help_text=help_text.PROJECT_ADMINS,
    )

    nomination_policy = models.CharField(
        max_length=12, default='Public', choices=(
            ('Public', "Public: anyone can nominate, even if they're not logged in."),
            ('Cobweb users', 'Cobweb users: anyone with a Cobweb account can nominate.'),
            ('Restricted', 'Restricted: only selected users can nominate.'),
        )
    )

    nominator_orgs = models.ManyToManyField(
        'core.Organization', blank=True,
        related_name='projects_nominating',
    )

    nominators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True,
        related_name='projects_nominating',
        help_text=help_text.PROJECT_NOMINATORS,
    )

    nominator_blacklist = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='projects_blacklisted',
        help_text=help_text.PROJECT_NOMINATOR_BLACKLIST,
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def impact_factor(self) -> int:
        # TODO: Fix this stub – not sure I understand the FRs...
        return self.nominations.exclude(claims=None).count()
    

    tags = models.ManyToManyField('core.Tag', blank=True, help_text=help_text.TAGS)
    subject_headings = models.ManyToManyField('core.SubjectHeading',
                                              blank=True)

    notes = GenericRelation('core.Note', blank=True)

    def get_absolute_url(self) -> str:
        return reverse('project', kwargs={'slug': self.slug})

    def get_add_nomination_url(self) -> str:
        return reverse('nomination_create', kwargs={'project_slug': self.slug})

    def is_admin(self, user: AbstractBaseUser) -> bool:
        return user in self.administrators.all()

    def is_nominator(self, user: AbstractBaseUser) -> bool:
        if self.is_admin(user):
            return True
        elif user in self.nominator_blacklist.all():
            return False
        else:
            return (user in self.nominators.all()
                    or self.nomination_policy == 'Public'
                    or (self.nomination_policy == 'Cobweb Users' and user.is_authenticated))

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

    @property
    def name(self):
        return self.title

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Project(pk={self.pk}, title={self.title})'


@reversion.register()
class Nomination(models.Model):
    class Meta:
        unique_together = ('resource', 'project')

    resource = models.ForeignKey(
        'core.Resource',
        on_delete=models.PROTECT,
        related_name='nominations',
        verbose_name='URL',
    )
    project = models.ForeignKey(Project, related_name='nominations',
                                on_delete=models.CASCADE)

    # ABOUT THE RESOURCE

    title = models.CharField(max_length=200, null=True, blank=True)
    creator = models.CharField(max_length=200, null=True, blank=True)
    language = models.ForeignKey('languages_plus.Language', null=True, blank=True,
                                 on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('core.Tag', blank=True, help_text=help_text.TAGS)
    subject_headings = models.ManyToManyField('core.SubjectHeading', blank=True)
    
    # TODO: setup required - see https://github.com/cordery/django-languages-plus
    
    # ABOUT THE NOMINATION

    # STATUS
    # needs_claim = models.BooleanField(default=True)
    @property
    def needs_claim(self):
        return self.claims.count() == 0

    nominated_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    rationale = models.TextField(null=True, blank=True,
                                 help_text=help_text.NOMINATION_RATIONALE)

    # CRAWL SCOPE - SIMPLE FIELDS
    # TODO: more complicated data w/ linked model
    crawl_start_date = models.DateField(null=True, blank=True)
    crawl_end_date = models.DateField(null=True, blank=True)
    crawl_frequency = models.CharField(
        null=True, blank=True, max_length=50,
        choices=[(x, x) for x in ("one time", "twice daily", "daily", "weekly",
                                  "monthly", "quarterly", "annually")]
    )

    intended_crawling_tool = models.CharField(
        null=True, blank=True, max_length=50,
        verbose_name="Crawling tool",
        choices=[(x, x) for x in ("Archive-It", "Brozzler", "Heritrix 1",
                                  "Heritrix 3", "Webrecorder", "Other")],
    )

    follow_links = models.IntegerField(null=True, blank=True, choices=[(1, 1), (2, 2)])
    page_scope = models.CharField(
        null=True, blank=True, max_length=50,
        choices=[(x, x) for x in ('Page', 'Domain')]
    )

    ignore_robots_txt = models.BooleanField(verbose_name="ignore 'robots.txt'",
                                            default=False)
    rights_considerations = models.TextField(verbose_name="access considerations",
                                             null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    notes = GenericRelation('core.Note')

    @property
    def impact_factor(self) -> int:
        return (self.endorsements.count() + self.claims.count() +
                self.claims.filter(has_holding=True).count())

    @property
    def name(self) -> str:
        return self.title or str(self.resource)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f'<Nomination {self.name} project={self.project}>'

    def can_claim(self, user: AbstractBaseUser) -> bool:
        """
        Return True if user can make a *new* claim on the object.

        Can be false if either the user is not affiliated with a claiming
        organization, or if the user's organization has already claimed self.
        """
        return (
            hasattr(user, 'organization')
            and (user.organization is not None)
            and (self.claims.filter(organization=user.organization).count() == 0)
        )

    def get_absolute_url(self) -> str:
        return reverse(
            'nomination_update',
            kwargs={'project_slug': self.project.slug, 'url': self.resource.url},
        )

    def get_edit_url(self) -> str:
        return reverse('nomination_update', kwargs={
            'project_slug': self.project.slug,
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
        if self.needs_claim:
            return 'unclaimed'
        elif not self.has_holding:
            return 'claimed'
        else:
            return 'held'

    def is_admin(self, user: AbstractBaseUser) -> bool:
        return user.is_authenticated and self.project.is_nominator(user)


@reversion.register()
class Claim(models.Model):
    class Meta:
        unique_together = ('nomination', 'organization')

    nomination = models.ForeignKey(Nomination, related_name='claims',
                                   on_delete=models.CASCADE)

    organization = models.ForeignKey('core.Organization', related_name='claims',
                                     null=False, blank=False, on_delete=models.PROTECT)

    # STATUS
    has_holding = models.BooleanField(default=False, verbose_name="held",
                                      help_text=help_text.CLAIM_HELD)

    imported_record = models.ForeignKey('webarchives.ImportedRecord', null=True, blank=True,
                                        on_delete=models.SET_NULL, related_name='claims')

    crawl_scope = models.ForeignKey('core.CrawlScope', null=True, blank=True,
                                    on_delete=models.CASCADE)

    # CRAWL SCOPE - SIMPLE FIELDS
    # TODO: more complicated data w/ linked model
    crawl_start_date = models.DateField(null=True, blank=True)
    crawl_end_date = models.DateField(null=True, blank=True)
    crawl_frequency = models.CharField(
        null=True, blank=True, max_length=50,
        choices=[(x, x) for x in ("one time", "twice daily", "daily", "weekly",
                                  "monthly", "quarterly", "annually")]
    )

    intended_crawling_tool = models.CharField(
        null=True, blank=True, max_length=50,
        verbose_name="Crawling tool",
        choices=[(x, x) for x in ("Archive-It", "Brozzler", "Heritrix 1",
                                  "Heritrix 3", "Webrecorder", "Other")],
    )

    follow_links = models.IntegerField(null=True, blank=True, choices=[(1, 1), (2, 2)])
    page_scope = models.CharField(
        null=True, blank=True, max_length=50,
        choices=[(x, x) for x in ('Page', 'Domain')]
    )

    ignore_robots_txt = models.BooleanField(verbose_name="ignore 'robots.txt'",
                                            default=False)
    rights_considerations = models.TextField(verbose_name="access considerations",
                                             null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    notes = GenericRelation('core.Note')

    @property
    def impact_factor(self) -> int:
        if self.has_holding:
            return 2
        else:
            return 1

    @property
    def name(self) -> str:
        return self.make_name(sep=' - ')

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<Claim {self.pk}>'

    def get_absolute_url(self) -> str:
        return reverse('claim', kwargs={'pk': self.pk})

    def get_edit_url(self) -> str:
        return reverse('claim_update', kwargs={'pk': self.pk})

    def make_name(self, exclude=set(), sep='\n'):
        return sep.join(str(f) for f in (
            self.nomination.resource.url,
            self.organization,
            self.nomination.project,
        ) if f not in exclude)

    def get_resource_set(self) -> QuerySet:
        return self.nomination.project

    def is_admin(self, user: AbstractBaseUser) -> bool:
        return self.organization.is_admin(user)  # or self.nomination.is_admin(user)
