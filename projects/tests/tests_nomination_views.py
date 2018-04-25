from django.test import TestCase
from lxml import html
import pytest

from projects.tests.factories import NominationFactory, ClaimFactory


@pytest.mark.django_db
class TestNominationDetailView:

    def test_loads(self, client):
        response = client.get(NominationFactory().get_absolute_url())
        assert response.status_code == 200

    @pytest.mark.xfail(strict=True)
    def test_all_claims_listed(self, client):
        nomination = NominationFactory()
        for _ in range(5):
            nomination.claims.add(ClaimFactory())

        response = client.get(nomination.get_absolute_url())
        tree = html.fromstring(response.content)

        for claim in nomination.claims.all():
            url = claim.get_absolute_url()
            assert len(tree.xpath(f'//a[@href="{url}"]')) == 1


class NominationCreateViewTests(TestCase):

    def setUp(self):
        pass

    def test_anonymous_cannot_nominate_to_restricted_project(self):
        pass

    def test_user_creates_project(self):
        """...
        Should autmatically set: User"""
        pass
