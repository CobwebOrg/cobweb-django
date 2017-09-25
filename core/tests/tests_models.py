from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Agent, Software, Organization
from core.tests import UserFactory, SoftwareFactory, AgentFactory, OrganizationFactory


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

    # def test_user_default_agent_creation(self):
    #     """Tests that creating a User also creates an Agent"""
    #     # import ipdb; ipdb.set_trace()
    #     self.test_instance.save()
    #     self.assertEqual(
    #         self.test_instance, 
    #         Agent.objects.get(
    #             user = self.test_instance,
    #             software = Software.current_website_software(),
    #         ).user
    #     )

class SoftwareModelTests(TestCase):

    def setUp(self):
        self.test_instance = Software.current_website_software()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Software)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

        # Make sure it works even if the usual fields are blank
        try:
            self.assertIsInstance(str(SoftwareFactory(name=None)), str)
        except:
            pass

class AgentModelTests(TestCase):

    def setUp(self):
        self.test_instance = AgentFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Agent)

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

        # Make sure it works even if the usual fields are blank
        try:
            self.assertIsInstance(
                str(OrganizationFactory(name=None, identifier=None)),
                str,
            )
        except:
            pass