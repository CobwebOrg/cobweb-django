import factory

from django.contrib.auth import get_user_model

from core.models import Organization


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ['username']

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
