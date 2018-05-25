"""SearchIndex classes for Django-haystack."""

from haystack import indexes

from projects.models import Project, Nomination, Claim


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    """Django-haystack index of Project model."""

    text = indexes.CharField(document=True, use_template=True, stored=False)

    title = indexes.CharField(model_attr='title', indexed=True, stored=True)
    description = indexes.CharField(model_attr='description', indexed=True, stored=True)
    # administrators
    nomination_policy = indexes.CharField(model_attr='nomination_policy', indexed=True, stored=True)
    # nominator_orgs
    # nominatorsdo
    # nominator_blacklist
    status = indexes.CharField(model_attr='status', indexed=True, stored=True)
    impact_factor = indexes.IntegerField(model_attr='impact_factor', indexed=True, stored=True)
    # tags
    # subject_headings
    # notes
    unclaimed_nominations = indexes.IntegerField(model_attr='n_unclaimed', indexed=True, stored=True)
    claimed_nominations = indexes.IntegerField(model_attr='n_claimed', indexed=True, stored=True)
    held_nominations = indexes.IntegerField(model_attr='n_held', indexed=True, stored=True)

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(status='Deleted')


class NominationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)

    project_pk = indexes.IntegerField(model_attr='project__pk', indexed=True, stored=True)
    url = indexes.CharField(model_attr='resource__url')
    
    status = indexes.CharField(model_attr='status', indexed=True, stored=True)
    # needs_claim = indexes.BooleanField(model_attr='needs_claim', indexed=True, stored=True)
    # deleted = indexes.(model_attr='deleted', indexed=True, stored=True)
    # nominated_by = indexes.MultiValueField(model_attr='nominated_by', indexed=True, stored=True)
    # rationale = indexes.(model_attr='rationale', indexed=True, stored=True)
    # suggested_crawl_frequency = indexes.(model_attr='suggested_crawl_frequency', indexed=True, stored=True)
    # suggested_crawl_end_date = indexes.(model_attr='suggested_crawl_end_date', indexed=True, stored=True)
    # notes = indexes.(model_attr='notes', indexed=True, stored=True)

    # impact_factor = indexes.IntegerField(model_attr='impact_factor', indexed=True, stored=True)
    

    def get_model(self):
        return Nomination

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(deleted__exact=True)


class ClaimIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)

    class Meta:
        model = Claim