from django.db.utils import IntegrityError
from django.test import TestCase

from core.models import User, Organization, Tag, Resource
from core.tests.factories import (UserFactory, OrganizationFactory, TagFactory,
                                  ResourceFactory)


class UserModelTests(TestCase):

    def setUp(self):
        self.test_instance = UserFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, User)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)


class OrganizationModelTests(TestCase):

    def setUp(self):
        self.test_instance = OrganizationFactory()

    def test_organization_creation(self):
        """Tests creation of Organization objects"""

        self.assertIsInstance(self.test_instance, Organization)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)


class TagModelTests(TestCase):

    def setUp(self):
        self.test_instance = TagFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Tag)

    def test_str(self):
        self.assertIsInstance(str(self.test_instance), str)


class ResourceModelTests(TestCase):

    def setUp(self):
        self.test_instance = ResourceFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Resource)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

        # Make sure it works or db rejects if the usual fields are blank
        try:
            self.assertIsInstance(str(ResourceFactory(url=None)), str)
        except IntegrityError:
            pass
