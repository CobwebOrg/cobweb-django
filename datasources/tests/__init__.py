import factory 

from core.tests import OrganizationFactory

from datasources import models


class APIEndpointFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.APIEndpoint

    location = factory.Faker('url')
    organization = factory.SubFactory(OrganizationFactory)

class AITPartnerImporterFactory(factory.Factory):
    class Meta:
        model = models.AITPartnerImporter

    api = factory.SubFactory(APIEndpointFactory, 
        location = 'https://archive-it.org/oai/organizations/853')