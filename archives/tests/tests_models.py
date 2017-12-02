from django.test import TestCase
from django.utils import timezone
import pytest

from webresources.tests import ResourceFactory

from archives.tests import CollectionFactory, ClaimFactory, HoldingFactory
from archives.models import Collection, Claim, Holding


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
        #     self.assertIsInstance(str(CollectionFactory(name=None)), str)
        # except:
        #     pass

    def test_https_becomes_http(self):
        self.test_instance.full_clean()
        self.assertTrue(self.test_instance.identifier.startswith('http://'))


class ClaimModelTests(TestCase):

    def setUp(self):
        self.test_instance = ClaimFactory(
            resource=ResourceFactory(),
            collection=CollectionFactory(),
            start_date=timezone.now(),
        )

    def test_claim_creation(self):
        """Tests creation of Claim objects"""

        self.assertTrue(isinstance(self.test_instance, Claim))

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)


@pytest.mark.django_db
def test_Claim_get_resource_set():
    """.get_resource_set() should return a collection object."""

    collection = CollectionFactory()
    assert ClaimFactory(collection=collection).get_resource_set() == collection


###########################
#   Holding Model Tests   #
###########################

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
def test_Claim_get_resource_set():
    """.get_resource_set() should return a collection object."""

    collection = CollectionFactory()
    assert HoldingFactory(collection=collection).get_resource_set() == collection
