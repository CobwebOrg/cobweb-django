from factory import DjangoModelFactory, Faker, SubFactory

from core.tests.factories import OrganizationFactory
from projects.models import Project, Nomination, Claim
from core.tests.factories import ResourceFactory


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
    # endorsements = SubFactory(UserFactory)


class ClaimFactory(DjangoModelFactory):
    class Meta:
        model = Claim

    nomination = SubFactory(NominationFactory)
    organization = SubFactory(OrganizationFactory)
