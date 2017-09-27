from django.test import TestCase

from metadata import models, tests


class MDVocabularyModelTests(TestCase):

    def setUp(self):
        self.test_instance = tests.MDVocabularyFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, models.MDVocabulary)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)



class MDPropertyModelTests(TestCase):

    def setUp(self):
        self.test_instances = [
            tests.MDPropertyFactory(),
            tests.MDPropertyFactory(vocabulary=None),
            tests.MDPropertyFactory(name=None),
        ]

    def test_creation(self):
        for instance in self.test_instances:
            self.assertIsInstance(instance, models.MDProperty)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        for instance in self.test_instances:
            self.assertIsInstance(str(instance), str)



class MetadatumModelTests(TestCase):

    def setUp(self):
        self.test_instances = [
            tests.MetadatumFactory(),
            tests.MetadatumFactory(md_property=None),
        ]

    def test_creation(self):
        for instance in self.test_instances:
            self.assertIsInstance(instance, models.Metadatum)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        for instance in self.test_instances:
            self.assertIsInstance(str(instance), str)
