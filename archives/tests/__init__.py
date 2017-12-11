from factory import DjangoModelFactory, Faker, SubFactory

from webresources.tests import ResourceFactory
from archives.models import Collection, Claim, Holding


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection
        # django_get_or_create = ('title')

    title = Faker('company')


class ClaimFactory(DjangoModelFactory):
    class Meta:
        model = Claim
        # django_get_or_create = ('resource', 'collection')

    resource = SubFactory(ResourceFactory)
    collection = SubFactory(CollectionFactory)
    start_date = Faker('date')


class HoldingFactory(DjangoModelFactory):
    class Meta:
        model = Holding
        # django_get_or_create = ('resource', 'collection')

    resource = SubFactory(ResourceFactory)
    collection = SubFactory(CollectionFactory)
