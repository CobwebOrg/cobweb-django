"""SearchIndex classes for Django-haystack."""
from typing import List, Iterable

from django.utils.html import format_html
from haystack import indexes
from haystack.exceptions import SearchFieldError

from core.models import User, Organization, Note, Tag, Resource
from projects.models import Project


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    """Django-haystack index of User model."""

    name = indexes.CharField(model_attr='name', indexed=True, stored=True)
    text = indexes.CharField(document=True, use_template=True)

    username = indexes.CharField(model_attr='username', 
                                 indexed=True, stored=True)
    first_name = indexes.CharField(model_attr='first_name', null=True,
                                   indexed=True, stored=True)
    last_name = indexes.CharField(model_attr='last_name', null=True,
                                  indexed=True, stored=True)

    email = indexes.CharField(model_attr='email', null=True,
                              indexed=True, stored=True)

    organization = indexes.CharField(
        model_attr='organization__get_absolute_url',
        null=True, indexed=True, stored=True
    )
    professional_title = indexes.CharField(model_attr='professional_title',
                                           null=True, indexed=True, stored=True)

    url = indexes.CharField(model_attr='url', null=True,
                            indexed=True, stored=True)

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return (
            self.get_model().objects.all()
            # .prefetch_related('organization')
        )


class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
    class Meta:
        model = Organization

    name = indexes.CharField(model_attr='name', indexed=True, stored=True)
    text = indexes.CharField(document=True, use_template=True)
    slug = indexes.CharField(model_attr='slug', indexed=True, stored=True)
    cobweb_url = indexes.CharField(model_attr='get_absolute_url', indexed=True, stored=True)

    short_name = indexes.CharField(model_attr='short_name', null=True, indexed=True, stored=True)
    administrators = indexes.CharField(indexed=True, null=True, stored=True)
    address = indexes.CharField(model_attr='address', null=True, indexed=True, stored=True)
    telephone_number = indexes.CharField(model_attr='telephone_number', null=True, indexed=True, stored=True)
    url = indexes.CharField(model_attr='url', null=True, indexed=True, stored=True)
    email_address = indexes.CharField(model_attr='email_address', null=True, indexed=True, stored=True)

    contact = indexes.CharField(model_attr='contact__get_absolute_url',
                                null=True, indexed=True, stored=True)
    parent_organization = indexes.CharField(
        model_attr='parent_organization__get_absolute_url',
        null=True, indexed=True, stored=True
    )

    description = indexes.CharField(model_attr='description', null=True, indexed=True, stored=True)
    identifier = indexes.CharField(model_attr='identifier', null=True, indexed=True, stored=True)

    def get_model(self):
        return Organization

    def index_queryset(self, using=None):
        return (
            self.get_model().objects.all()
            .prefetch_related('contact', 'parent_organization')
        )

    def prepare_administrators(self, obj: Organization) -> str:
        return '\n'.join(user.get_absolute_url() for user in obj.administrators.all())



class ResourceIndex(indexes.SearchIndex, indexes.Indexable):
    class Meta:
        model = Resource

    name = indexes.CharField(model_attr='url', stored=True, indexed=False)
    text = indexes.CharField(document=True, use_template=True) 

    url = indexes.CharField(model_attr='url', stored=True, indexed=True)
    title = indexes.CharField(null=True, stored=True, indexed=True)

    # status = indexes.CharField(stored=True, indexed=True)
    description = indexes.CharField(null=True, stored=True, indexed=True)
    language = indexes.CharField(null=True, stored=True, indexed=True) 
    tags = indexes.MultiValueField(null=True, stored=True, indexed=True)
    subject_headings = indexes.MultiValueField(null=True, stored=True, indexed=True)

    def get_model(self):
        return Resource

    def index_queryset(self, using=None):
        return (
            self.get_model().objects.all()
            .prefetch_related('nominations', 'imported_records')
        )

    def prepare_title(self, obj: Resource) -> str:
        titles = {n.title for n in obj.nominations.all()}
        for r in obj.imported_records.all():
            if 'title' in r.metadata:
                titles.update(r.metadata['title'])
        return '\n'.join(x for x in titles if x)

    def prepare_description(self, obj: Resource) -> str:
        descriptions = {n.description for n in obj.nominations.all()}
        for r in obj.imported_records.all():
            if 'description' in r.metadata:
                descriptions.update(r.metadata['description'])
        return '\n'.join(x for x in descriptions if x)

    def prepare_language(self, obj: Resource) -> str:
        languages = {n.language.name for n in obj.nominations.all() if n.language}
        for r in obj.imported_records.all():
            if 'language' in r.metadata:
                languages.update(r.metadata['language'])
        return '\n'.join(x for x in languages if x)

    def prepare_tags(self, obj: Resource) -> str:
        tags = set()
        for nom in obj.nominations.all():
            tags.update({t.name for t in nom.tags.all()})
        for rec in obj.imported_records.all():
            try:
                tags.update(rec.metadata['tags'])
            except KeyError:
                pass
        return ','.join(x for x in tags if x)

    def prepare_subject_headings(self, obj: Resource) -> str:
        subject_headings = set()
        for nom in obj.nominations.all():
            subject_headings.update({t.name for t in nom.subject_headings.all()})
        for rec in obj.imported_records.all():
            try:
                subject_headings.update(rec.metadata['subject_headings'])
            except KeyError:
                pass
        return ','.join(x for x in subject_headings if x)




# class NoteIndex(indexes.ModelSearchIndex, indexes.Indexable):
#     class Meta:
#         model = Note
        
#     name = indexes.CharField(model_attr='name', indexed=True, stored=True)
#     text = indexes.CharField(document=True, use_template=False)


# class ResourceIndex(indexes.ModelSearchIndex, indexes.Indexable):
#     """Django-haystack index of Resource model."""
    
#     class Meta:
#         model = Resource
