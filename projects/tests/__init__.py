from factory import DjangoModelFactory, Faker, SubFactory

from core.tests import UserFactory
from webresources.tests import ResourceFactory

from archives.tests import CollectionFactory
from projects.models import Project, Nomination, Claim


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    title = Faker('sentence')
    description = Faker('paragraph')


class NominationFactory(DjangoModelFactory):
    class Meta:
        model = Nomination
        # django_get_or_create = ( 'resource', 'project', 'nominated_by' )

    resource = SubFactory(ResourceFactory)
    project = SubFactory(ProjectFactory)
    nominated_by = SubFactory(UserFactory)


class ClaimFactory(DjangoModelFactory):
    class Meta:
        model = Claim
        # django_get_or_create = ('resource', 'collection')

    resource = SubFactory(ResourceFactory)
    collection = SubFactory(CollectionFactory)
    start_date = Faker('date')
