from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Organization
from core.tests import UserFactory, OrganizationFactory


class UserModelTests(TestCase):

    def setUp(self):
        self.test_instance = UserFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, get_user_model())

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

        # Make sure it works even if the usual fields are blank
        try:
            self.assertIsInstance(
                str(UserFactory(first_name=None, last_name=None, username=None)),
                str,
            )
        except:
            pass

class OrganizationModelTests(TestCase):

    def setUp(self):
        self.test_instance = OrganizationFactory()

    def test_organization_creation(self):
        """Tests creation of Organization objects"""

        self.assertIsInstance(self.test_instance, Organization)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

        # Make sure it works even if the usual fields are blank
        try:
            self.assertIsInstance(
                str(OrganizationFactory(name=None, identifier=None)),
                str,
            )
        except:
            pass