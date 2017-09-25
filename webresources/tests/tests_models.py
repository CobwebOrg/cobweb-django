from django.db.utils import IntegrityError
from django.test import TestCase

from webresources.models import Resource
from webresources.tests import ResourceFactory

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
            self.assertIsInstance(str(ResourceFactory(location=None)), str)
        except IntegrityError:
            pass