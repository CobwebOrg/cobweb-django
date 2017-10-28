from django.test import TestCase

from datasources import models, tests

### test that importing an archive-it subcollection doesn't reset collection 
### name or create a new collection

class AITPartnerImporterTests(TestCase):

    def setUp(self):
        self.importer = tests.AITPartnerImporterFactory()

    def test___harvest_setspec__(self):
        pass

    def test___get_set_identifier__(self):
        self.assertEqual(
            self.importer.__get_set_identifier__('collection:8033'),
            'http://archive-it.org/collections/8033'
        )
        self.assertEqual(
            self.importer.__get_set_identifier__('organization:853'),
            'http://archive-it.org/organizations/853'
        )
        self.assertEqual(
            self.importer.__get_set_identifier__('organization'),
            None
        )