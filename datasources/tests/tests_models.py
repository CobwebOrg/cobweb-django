from django.contrib.auth import get_user_model
from django.test import TestCase

from datasources import models, tests


class APIEndpointModelTests(TestCase):

    def setUp(self):
        self.test_instance = tests.APIEndpointFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, models.APIEndpoint)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

    def test_get_archiveit_root(self):
        ait = models.APIEndpoint.get_archiveit_root()
        self.assertIsInstance(ait, models.APIEndpoint)
        self.assertEqual(ait.location, 'https://archive-it.org/oai')

    def test_get_agent(self):
        agent = self.test_instance.get_agent()
        self.assertIsInstance(agent, get_user_model())

    def test_get_importer(self):
        importer = ( tests
            .APIEndpointFactory(importer_class_name='OAIPMHImporter')
            .get_importer()
        )
        self.assertTrue( issubclass(type(importer), models.Importer) )
        self.assertIsInstance(importer, models.importers['OAIPMHImporter'])

        importer = ( tests
            .APIEndpointFactory(importer_class_name='AITCollectionsImporter')
            .get_importer()
        )
        self.assertTrue( issubclass(type(importer), models.Importer) )
        self.assertIsInstance(importer, models.importers['OAIPMHImporter'])
