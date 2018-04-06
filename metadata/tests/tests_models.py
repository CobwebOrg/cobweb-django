import django.test

from metadata import models
from metadata.tests.factories import TagFactory


class TagModelTests(django.test.TestCase):

    def setUp(self):
        self.test_instance = TagFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, models.Tag)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)
