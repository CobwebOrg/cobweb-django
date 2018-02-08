from django.test import TestCase
from django.utils import timezone
import pytest

from core.tests.factories import UserFactory
from webresources.tests.factories import ResourceFactory

from archives.tests.factories import CollectionFactory, HoldingFactory
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

    # Expect to fail because I'm using a stopgap is_admin that always returns true for orphan Collections
    @pytest.mark.xfail(strict=True)
    def test_is_admin(self):
        collection = CollectionFactory()
        user = UserFactory()
        assert collection.is_admin(user) is False

        collection.administrators.add(user)
        assert collection.is_admin(user) is True

    # This one tests the stopgap behavior and should be removed when it is.
    def test_is_admin(self):
        collection = CollectionFactory()
        user = UserFactory()
        assert collection.is_admin(user) is True

        collection.administrators.add(user)
        assert collection.is_admin(user) is True

        assert collection.is_admin(UserFactory()) is False


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
