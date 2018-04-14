from factory import DjangoModelFactory, Faker, SubFactory

from core.tests.factories import ResourceFactory
from archives.models import Collection, Holding


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection
        # django_get_or_create = ('title')

    title = Faker('company')


class HoldingFactory(DjangoModelFactory):
    class Meta:
        model = Holding
        # django_get_or_create = ('resource', 'collection')

    resource = SubFactory(ResourceFactory)
    collection = SubFactory(CollectionFactory)
