from django.test import TestCase
from django.utils import timezone
import pytest

from webresources.tests import ResourceFactory

from archives.tests import CollectionFactory, HoldingFactory
from archives.models import Collection, Holding


class CollectionModelTests(TestCase):

    def setUp(self):
        self.test_instance = CollectionFactory(
            identifier="https://testurl.test/test"
        )

    def test_collection_creation(self):
        self.assertTrue(isinstance(self.test_instance, Collection))

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

        # # Make sure it works even if the usual fields are blank
        # try:
        #     self.assertIsInstance(str(CollectionFactory(title=None)), str)
        # except:
        #     pass

    def test_https_becomes_http(self):
        self.test_instance.full_clean()
        self.assertTrue(self.test_instance.identifier.startswith('http://'))


class HoldingModelTests(TestCase):

    def setUp(self):
        self.test_instance = HoldingFactory(
            resource=ResourceFactory(),
            collection=CollectionFactory(),
        )

    def test_holding_creation(self):
        """Tests creation of Holding objects"""

        self.assertTrue(isinstance(self.test_instance, Holding))

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)


@pytest.mark.django_db
def test_Holding_get_resource_set():
    """.get_resource_set() should return a collection object."""

    collection = CollectionFactory()
    assert HoldingFactory(collection=collection).get_resource_set() == collection
