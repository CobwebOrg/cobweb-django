import unittest
from pathlib import Path
from unittest import mock

import pytest
from django import test
from django.conf import settings

from archives.models import Collection, Holding
from core.models import Organization
from datasources import models
from datasources.tests.factories import AITPartnerImporterFactory


### test that importing an archive-it subcollection doesn't reset collection
### name or create a new collection

def test_OAIPMHImporter_harvest_record_transfers_title():
    pass

class AITPartnerImporterTests(test.TestCase):

    def setUp(self):
        self.importer = AITPartnerImporterFactory()

    def test___harvest_setspec(self):
        pass

    def test___get_set_identifier(self):
        self.assertEqual(
            self.importer.get_set_identifier('collection:8033'),
            'http://archive-it.org/collections/8033'
        )
        self.assertEqual(
            self.importer.get_set_identifier('organization:853'),
            'http://archive-it.org/organizations/853'
        )
        self.assertEqual(
            self.importer.get_set_identifier('organization'),
            None
        )


def fake_get(url, params):
    verb = params['verb']
    doc = Path(settings.BASE_DIR + f'/datasources/tests/sample/{verb}.xml').read_text()
    return doc


@pytest.mark.skip
@pytest.mark.django_db
@mock.patch('sickle.app.requests.get', fake_get)
def test_ait_partner_importer():
    api = AITPartnerImporterFactory()
    api.harvest()

#
# # Path('').read_text
# @pytest.mark.django_db
# @mock.patch.object('sickle.Sickle')
# def test_mocked_sickle(mock_get):
# api = AITPartnerImporterFactory()
# with pytest.raises(ValueError):
#     api.harvest()
# mock_get.assert_called()


@unittest.skip("Takes too long, already passed.")
class LiveArchiveItTests(test.TestCase):

    def test_names_and_identifiers(self):
        models.APIEndpoint.get_archiveit_root().harvest()

        self.harvard = Organization.objects.get(
            identifier='http://archive-it.org/organizations/935')
        self.ucla = Organization.objects.get(
            identifier='http://archive-it.org/organizations/877')

        self.harvard_collection = Collection.objects.get(
            identifier='http://archive-it.org/collections/5456')
        self.ucla_collection = Collection.objects.get(
            identifier='http://archive-it.org/collections/7397')

        self.harvard.apiendpoint_set.first().harvest()
        self.ucla.apiendpoint_set.first().harvest()

        self.harvard_holding = Holding.objects.get(
            collection=self.harvard_collection,
            resource__url='http://library.harvard.edu/')
        self.ucla_holding = self.ucla_collection.holdings.get(
            resource__url__icontains='labour.org.uk/inforbritain')

        self.assertEqual(
            self.harvard_holding.collection.organization.identifier,
            'http://archive-it.org/organizations/935',
        )
        self.assertEqual(
            self.ucla_holding.collection.organization.identifier,
            'http://archive-it.org/organizations/877',
        )
        self.assertEqual(
            self.harvard_holding.collection.identifier,
            'http://archive-it.org/collections/5456',
        )
        self.assertEqual(
            self.ucla_holding.collection.identifier,
            'http://archive-it.org/collections/7397',
        )

        self.assertEqual(
            self.harvard_holding.collection.organization.name,
            'Harvard University Archives',
        )
        self.assertEqual(
            self.ucla_holding.collection.organization.name,
            'UCLA',
        )
        self.assertEqual(
            self.harvard_holding.collection.title,
            'A-Sites: Archived Harvard Websites',
        )
        self.assertEqual(
            self.ucla_holding.collection.title,
            'UK European Union Membership Referendum',
        )
