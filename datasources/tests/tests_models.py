from unittest import mock
from django.contrib.auth import get_user_model
from django.test import TestCase

from datasources import models
from datasources.tests.factories import APIEndpointFactory


class APIEndpointModelTests(TestCase):

    def setUp(self):
        self.test_instance = APIEndpointFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, models.APIEndpoint)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

    def test_get_archiveit_root(self):
        ait = models.APIEndpoint.get_archiveit_root()
        assert isinstance(ait, models.APIEndpoint)
        assert ait.location == 'https://archive-it.org/oai'

    def test_get_importer(self):
        importer = (APIEndpointFactory(importer_class_name='OAIPMHImporter')
                    .get_importer())
        self.assertTrue( issubclass(type(importer), models.Importer) )
        self.assertIsInstance(importer, models.importers['OAIPMHImporter'])

        importer = (APIEndpointFactory(importer_class_name='AITCollectionsImporter')
                    .get_importer())
        self.assertTrue( issubclass(type(importer), models.Importer) )
        self.assertIsInstance(importer, models.importers['OAIPMHImporter'])
