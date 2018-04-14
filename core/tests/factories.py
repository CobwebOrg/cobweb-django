import factory

from core.models import User, Organization, Tag


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


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = Faker('word')
