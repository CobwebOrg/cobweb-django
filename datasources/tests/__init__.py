import factory 

from core.tests import OrganizationFactory

from datasources import models


class APIEndpointFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.APIEndpoint

    location = factory.Faker('url')
    organization = factory.SubFactory(OrganizationFactory)
    