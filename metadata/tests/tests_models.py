from django.test import TestCase

from metadata import models, tests


class KeywordModelTests(TestCase):

    def setUp(self):
        self.test_instance = tests.KeywordFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, models.Keyword)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)
        
