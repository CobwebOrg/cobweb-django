"""SearchIndex classes for Django-haystack."""

from haystack import indexes

from archives.models import Collection
from core.models import User, Organization, Note
from projects.models import Project
from core.models import Resource


class UserIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of User model."""

    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = User


class OrganizationIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Organization model."""

    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Organization


class NoteIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)

    class Meta:
        model = Note


class ResourceIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Resource model."""

    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Resource

