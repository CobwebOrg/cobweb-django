"""SearchIndex classes for Django-haystack."""

from django.utils.html import format_html
from haystack import indexes

from core.models import User, Organization, Note, Tag, Resource
from projects.models import Project


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    """Django-haystack index of User model."""

    name = indexes.CharField(model_attr='name', indexed=True, stored=True)
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class OrganizationIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """Django-haystack index of Organization model."""

    name = indexes.CharField(model_attr='name', indexed=True, stored=True)
    text = indexes.CharField(document=True, use_template=True)

    class Meta:
        model = Organization


# class NoteIndex(indexes.ModelSearchIndex, indexes.Indexable):
#     class Meta:
#         model = Note
        
#     name = indexes.CharField(model_attr='name', indexed=True, stored=True)
#     text = indexes.CharField(document=True, use_template=False)


# class ResourceIndex(indexes.ModelSearchIndex, indexes.Indexable):
#     """Django-haystack index of Resource model."""
    
#     class Meta:
#         model = Resource
