"""SearchIndex classes for Django-haystack."""

from haystack import indexes

from archives.models import Collection
from core.models import User, Organization, Note
from projects.models import Project
from core.models import Resource


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

