"""SearchIndex classes for Django-haystack."""


from haystack import indexes

from archives.models import Collection
from core.models import User, Organization
from projects.models import Project
from webresources.models import Resource


class ProjectIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Project model."""

    class Meta:
        """ProjectIndex metaclass."""

        model = Project
        excludes = ['nominator_blacklist']

    def index_queryset(self, using=None):
        """
        Use to update the entire index for model.

        Excludes projects whose status is 'deleted'.
        """
        return self.get_model().objects.exclude(status='d')


class CollectionIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Collection model."""

    class Meta:
        """CollectionIndex metaclass."""

        model = Collection


class ResourceIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Resource model."""

    class Meta:
        """ResourceIndex metaclass."""

        model = Resource


class UserIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of User model."""

    class Meta:
        """UserIndex metaclass."""

        model = User


class OrganizationIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Organization model."""

    class Meta:
        """OrganizationIndex metaclass."""

        model = Organization
