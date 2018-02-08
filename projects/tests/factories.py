from factory import DjangoModelFactory, Faker, SubFactory

from archives.tests.factories import CollectionFactory
from projects.models import Project, Nomination, Claim
from webresources.tests.factories import ResourceFactory


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    title = Faker('sentence')
    description = Faker('paragraph')


class NominationFactory(DjangoModelFactory):
    class Meta:
        model = Nomination

    resource = SubFactory(ResourceFactory)
    project = SubFactory(ProjectFactory)
    # nominated_by = SubFactory(UserFactory)


class ClaimFactory(DjangoModelFactory):
    class Meta:
        model = Claim
        # django_get_or_create = ('resource', 'collection')

    nomination = SubFactory(NominationFactory)
    collection = SubFactory(CollectionFactory)
