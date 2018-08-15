"""SearchIndex classes for Django-haystack."""
from typing import List

from django.utils.html import format_html
from haystack import indexes
from haystack.exceptions import SearchFieldError

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

class ResourceIndex(indexes.SearchIndex, indexes.Indexable):
    class Meta:
        model = Resource

    # name = indexes.CharField(model_attr='name', stored=True, indexed=False)
    text = indexes.CharField(model_attr='data', document=True, use_template=False) 

    url = indexes.CharField(model_attr='url', stored=True, indexed=True)
    title = indexes.CharField(stored=True, indexed=True)

    # status = indexes.CharField(stored=True, indexed=True)
    # description = indexes.CharField(stored=True, indexed=True)
    # language = indexes.CharField(stored=True, indexed=True) 
    # tags = indexes.MultiValueField(stored=True, indexed=True)
    # subject_headings = indexes.MultiValueField(stored=True, indexed=True)

    def get_model(self):
        return Resource

    def index_queryset(self, using=None):
        return (
            self.get_model().objects.all()
            .prefetch_related('resource_scans', 'resource_descriptions')
        )

    # def prepare_title(self, obj: Resource) -> List[str]:
    #     try:
    #         return obj.data['title'].join(' / ')
    #     except KeyError:
    #         return []

    # def prepare_status(self, obj: Resource) -> List[str]:
    #     try:
    #         return obj.data['status'].join(' / ')
    #     except KeyError:
    #         return []

    # def prepare_description(self, obj: Resource) -> List[str]:
    #     try:
    #         return obj.data['description'].join('\n')
    #     except KeyError:
    #         return []

    # def prepare_language(self, obj: Resource) -> List[str]:
    #     try:
    #         return obj.data['language'].join(' / ')
    #     except KeyError:
    #         return []

    # def prepare_tags(self, obj: Resource) -> List[str]:
    #     try:
    #         return obj.data['tags']
    #     except KeyError:
    #         return []

    # def prepare_subject_headings(self, obj: Resource) -> List[str]:
    #     try:
    #         return obj.data['subject_headings']
    #     except KeyError:
    #         return []




# class NoteIndex(indexes.ModelSearchIndex, indexes.Indexable):
#     class Meta:
#         model = Note
        
#     name = indexes.CharField(model_attr='name', indexed=True, stored=True)
#     text = indexes.CharField(document=True, use_template=False)


# class ResourceIndex(indexes.ModelSearchIndex, indexes.Indexable):
#     """Django-haystack index of Resource model."""
    
#     class Meta:
#         model = Resource
