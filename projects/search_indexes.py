from haystack import indexes

from projects.models import Project, Nomination


class ProjectIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Uses Django-haystack to create Solr index of Project model."""

    class Meta:
        """haystack.ModelSearchIndex metaclass."""

        model = Project
        excludes = ['nominator_blacklist']

    def index_queryset(self, using=None):
        """
        Use to update the entire index for model.

        Excludes projects whose status is 'deleted'.
        """
        return self.get_model().objects.exclude(status='d')


class NominationIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Uses Django-haystack to create Solr index of Nomination model."""

    class Meta:
        """haystack.ModelSearchIndex metaclass."""

        model = Nomination
