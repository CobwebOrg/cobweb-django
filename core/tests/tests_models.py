from django.test import TestCase

from core.models import User, Organization, Tag
from core.tests.factories import UserFactory, OrganizationFactory, TagFactory


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
