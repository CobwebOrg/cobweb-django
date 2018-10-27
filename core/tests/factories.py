import random

import factory
from django.utils.text import slugify
from languages_plus.models import Language

from core.models import User, Organization
from core.models import Note, Tag, SubjectHeading
from core.models import Resource


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    is_superuser = False


class OrganizationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Organization

    slug = factory.LazyAttribute(lambda org: slugify(org.full_name)[:50])
    full_name = factory.Faker('company')
    address = factory.Faker('address')
    description = factory.Faker('paragraph')


class NoteFactory(factory.DjangoModelFactory):
    class Meta:
        model = Note

    author = factory.SubFactory(UserFactory)
    ref = factory.SubFactory(OrganizationFactory)
    text = factory.Faker('paragraph')


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.Faker('word')


def add_tags(obj, create, extracted, **kwargs):
    """Add tags.

    cf.
    http://factoryboy.readthedocs.io/en/latest/recipes.html#simple-many-to-many-relationship
    """

    if not create:
        # Simple build, do nothing.
        return
    elif extracted:
        for tag in extracted:
            if isinstance(tag, str):
                tag = TagFactory(name=tag)
            obj.tags.add(tag)
    else:
        while random.random() > 0.8:
            obj.tags.add(TagFactory())


class SubjectHeadingFactory(factory.DjangoModelFactory):
    class Meta:
        model = SubjectHeading

    title = factory.Faker('word')


class ResourceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Resource
        django_get_or_create = ['url']

    url = factory.Faker('url')
