import factory

from core.models import User, Organization
from core.models import Note, Tag, SubjectHeading
from core.models import Resource, ResourceScan, ResourceDescription


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

    name = factory.Faker('company')
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

    name = factory.Faker('word')


class SubjectHeadingFactory(factory.DjangoModelFactory):
    class Meta:
        model = SubjectHeading

    name = factory.Faker('word')


class ResourceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Resource
        django_get_or_create = ['url']

    url = factory.Faker('url')


class ResourceDescriptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = ResourceDescription

    resource = factory.SubFactory(ResourceFactory)
    asserted_by = factory.SubFactory(UserFactory)

    # title = factory.Faker('')
    description = factory.Faker('paragraph')

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """Add tags.

        cf.
        http://factoryboy.readthedocs.io/en/latest/recipes.html#simple-many-to-many-relationship
        """
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for tag in extracted:
                if isinstance(tag, str):
                    tag = TagFactory(name=tag)
                self.tags.add(tag)


class ResourceScanFactory(factory.DjangoModelFactory):
    class Meta:
        model = ResourceScan

    resource = factory.SubFactory(ResourceFactory)
