import hypothesis
from hypothesis.extra.django import TestCase
import pytest
from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError

from archives.tests.factories import CollectionFactory
from core.tests.factories import UserFactory
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

    def test_is_admin(self):
        assert self.test_instance.is_admin(AnonymousUser()) is False
        user = UserFactory()
        assert self.test_instance.is_admin(user) is False
        self.test_instance.administrators.add(user)
        assert self.test_instance.is_admin(user) is True

    def test_is_nominator(self):
        # TODO: more complicated logic involving nomination_policy
        assert self.test_instance.is_nominator(AnonymousUser()) is False
        user = UserFactory()
        # assert self.test_instance.is_nominator(user) is False
        self.test_instance.nominators.add(user)
        assert self.test_instance.is_nominator(user) is True


class NominationModelTests(TestCase):

    def setUp(self):
        self.test_instance = NominationFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Nomination)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

    @hypothesis.given(hypothesis.strategies.text(alphabet=hypothesis.strategies.characters(min_codepoint=1), min_size=1))
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
        """.get_resource_set() should return a Project object."""

        project = ProjectFactory()
        nomination = NominationFactory(project=project)
        assert ClaimFactory(nomination=nomination).get_resource_set() == project

    def test_is_admin(self):
        # TODO: complicated logic -> vary project nomination policy &c
        claim = ClaimFactory()
        assert claim.is_admin(AnonymousUser()) is False

        user = UserFactory()

        claim.nomination.project.administrators.add(user)
        assert claim.is_admin(user) is True

        claim.nomination.project.administrators.remove(user)
        claim.collection.administrators.add(user)
        assert claim.is_admin(user) is True

        claim.nomination.project.administrators.add(user)
        assert claim.is_admin(user) is True

    def test_project(self):
        claim = ClaimFactory()
        assert claim.project == claim.nomination.project

    def test_project(self):
        claim = ClaimFactory()
        assert claim.project == claim.nomination.project

    def test_resource(self):
        claim = ClaimFactory()
        assert claim.resource == claim.nomination.resource

    def test_impact_factor(self):
        claim = ClaimFactory()
        claim.resource.holdings.delete()
