"""SearchIndex classes for Django-haystack."""

from haystack import indexes

from archives.models import Collection
from core.models import User, Organization, Note
from projects.models import Project
from webresources.models import Resource


class ProjectIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Project model."""

    text = indexes.CharField(document=True, use_template=True)

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

    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        """CollectionIndex metaclass."""

        model = Collection


class ResourceIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Resource model."""

    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        """ResourceIndex metaclass."""

        model = Resource


class UserIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of User model."""

    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        """UserIndex metaclass."""

        model = User


class OrganizationIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Organization model."""

    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        """OrganizationIndex metaclass."""

        model = Organization


class NoteIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Note

