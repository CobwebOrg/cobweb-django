"""Tests for models in the cobweb-django app "archives": Collection, Holding."""

from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
import pytest

from archives.tests.factories import CollectionFactory, HoldingFactory
from archives.models import Collection, Holding
from core.tests.factories import UserFactory


class TestCollectionModels(TestCase):
    """Tests for archives.models.Collection."""

    def setUp(self):
        """Attaches a Collection instance to the TestCase object."""
        self.test_instance = CollectionFactory()

    def test_collection_creation(self):
        """Collection can be created successfully."""
        self.assertTrue(isinstance(self.test_instance, Collection))

    def test_save(self):
        """Collection can be saved to db."""
        self.test_instance.save()

    def test_get_absolute_url(self):
        """get_edit_url returns the display url for Collection."""
        url = self.test_instance.get_absolute_url()
        assert url == f'/collections/{self.test_instance.pk}/'

    def test_get_edit_url(self):
        """get_edit_url returns the edit url for Collection."""
        url = self.test_instance.get_edit_url()
        assert url == f'/collections/{self.test_instance.pk}/edit'

    # Expect to fail because I'm using a stopgap is_admin that always returns
    # true for orphan Collections
    @pytest.mark.xfail(strict=True)
    def test_is_admin(self):
        """is_admin() returns true if and only if user is collection administrator."""
        collection = CollectionFactory()
        assert collection.is_admin(AnonymousUser()) is False

        user = UserFactory()
        assert collection.is_admin(user) is False

        collection.administrators.add(user)
        assert collection.is_admin(user) is True

    # This one tests the stopgap behavior and should be removed when it is.
    def test_interim_is_admin(self):  # noqa
        """
        is_admin() returns true if user is admin or there are none. ***DANGER***

        Tests an interim behavior that should be eliminated before production.
        """
        collection = CollectionFactory()
        assert collection.is_admin(AnonymousUser()) is False

        user = UserFactory()
        assert collection.is_admin(user) is True

        collection.administrators.add(user)
        assert collection.is_admin(user) is True

        assert collection.is_admin(UserFactory()) is False

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)


class HoldingModelTests(TestCase):
    """Tests for archives.models.Holding."""

    def setUp(self):
        """Create a test Holding instance."""
        self.test_instance = HoldingFactory()

    def test_holding_creation(self):
        """Tests creation of Holding objects."""
        assert isinstance(self.test_instance, Holding)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

    def test_get_resource_set(self):
        """Holding(...).get_resource_set() returns a Collection."""
        assert isinstance(self.test_instance.get_resource_set(), Collection)
