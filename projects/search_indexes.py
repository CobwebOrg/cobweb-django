"""SearchIndex classes for Django-haystack."""

from haystack import indexes

from archives.models import Collection
from projects.models import Project


class ProjectIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Project model."""

    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Project
        excludes = ['nominator_blacklist']

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(status='Deleted')

