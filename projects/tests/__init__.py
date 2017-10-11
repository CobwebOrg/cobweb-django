from factory import DjangoModelFactory, Faker, SubFactory

from core.tests import UserFactory
from webresources.tests import ResourceFactory

from projects.models import Project, Nomination


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = Faker('sentence')
    description = Faker('paragraph')

class NominationFactory(DjangoModelFactory):
    class Meta:
        model = Nomination
        # django_get_or_create = ( 'resource', 'project', 'nominated_by' )

    resource = SubFactory(ResourceFactory)
    project = SubFactory(ProjectFactory)
    nominated_by = SubFactory(UserFactory)
