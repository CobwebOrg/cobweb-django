from django.test import TestCase

from metadata.models import Keyword
from metadata.tests import KeywordFactory


class KeywordModelTests(TestCase):

    def setUp(self):
        self.test_instance = KeywordFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Keyword)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

        # Make sure it works even if the usual fields are blank
        try:
            self.assertIsInstance(str(SoftwareFactory(name=None)), str)
        except:
            pass