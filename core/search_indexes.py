"""SearchIndex classes for Django-haystack."""

from haystack import indexes

from core.models import User, Organization, Note, Tag, Resource
from projects.models import Project


class UserIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of User model."""

    name = indexes.CharField(indexed=True, stored=True)
    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = User


class OrganizationIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Organization model."""

    name = indexes.CharField(indexed=True, stored=True)
    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Organization


class NoteIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Note
        
    name = indexes.CharField(indexed=True, stored=True)
    text = indexes.CharField(document=True, use_template=False)


class ResourceIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Resource model."""

    name = indexes.CharField(indexed=True, stored=True)
    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Resource

