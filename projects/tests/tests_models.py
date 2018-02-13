import hypothesis
import pytest
from django.db.utils import IntegrityError
from django.test import TestCase

from archives.tests.factories import CollectionFactory
from projects.models import Project, Nomination, Claim
from projects.tests.factories import ProjectFactory, NominationFactory, ClaimFactory


class ProjectModelTests(TestCase):

    def setUp(self):
        self.test_instance = ProjectFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Project)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

    def test_is_nominator_function(self):
        pass


class NominationModelTests(TestCase):

    def setUp(self):
        self.test_instance = NominationFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Nomination)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

    @hypothesis.given(hypothesis.strategies.text(alphabet=hypothesis.strategies.characters(min_codepoint=1),
                                                 min_size=1, average_size=15))
    def test_name(self, title):
        """Nomination.name returns title if the nomination has one, otherwise url."""
        nomination = NominationFactory(title=None)
        assert nomination.name == nomination.resource.url and nomination.name[:4] == 'http'
        nomination.title = title
        assert nomination.name == title


@pytest.mark.django_db
class TestClaimModel:

    def test_claim_creation(self):
        """Tests creation of Claim objects"""

        good_claim_data = {'nomination': NominationFactory(),
                           'collection': CollectionFactory()}
        Claim.objects.create(**good_claim_data).save()

        # Duplicate data should raise error
        with pytest.raises(IntegrityError):
            Claim.objects.create(**good_claim_data)

    def test_create_with_incomplete_data(self):
        incomplete_data = {'nomination': NominationFactory()}
        with pytest.raises(IntegrityError):
            Claim.objects.create(**incomplete_data)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        assert isinstance(str(NominationFactory), str)

    def test_Claim_get_resource_set(self):
        """.get_resource_set() should return a collection object."""

        collection = CollectionFactory()
        assert ClaimFactory(collection=collection).get_resource_set() == collection
