import hypothesis
from hypothesis.extra.django import TestCase
import pytest
from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError

from core.tests.factories import UserFactory, OrganizationFactory
from projects.models import Project, Nomination, Claim
from projects.tests.factories import ProjectFactory, NominationFactory, ClaimFactory


class TestProjectModel:

    @pytest.mark.django_db
    def test_project_model(self):
        project = ProjectFactory()
        assert isinstance(project, Project)
        assert isinstance(str(project), str)

    @pytest.mark.django_db
    def test_is_admin(self):
        project = ProjectFactory()
        assert project.is_admin(AnonymousUser()) is False
        user = UserFactory()
        assert project.is_admin(user) is False
        project.administrators.add(user)
        assert project.is_admin(user) is True

    @pytest.mark.django_db
    def test_is_nominator(self):
        project = ProjectFactory()

        anon_user = AnonymousUser()

        blacklisted_user = UserFactory()
        project.nominator_blacklist.add(blacklisted_user)

        random_user = UserFactory()

        nominator_user = UserFactory()
        project.nominators.add(nominator_user)

        admin_user = UserFactory()
        project.administrators.add(admin_user)

        for nomination_policy, user, result in (
            ('Public', blacklisted_user, False),
            ('Public', anon_user, True),
            ('Public', random_user, True),
            ('Public', nominator_user, True),
            ('Public', admin_user, True),

            ('Cobweb Users', anon_user, False),
            ('Cobweb Users', blacklisted_user, False),
            ('Cobweb Users', random_user, True),
            ('Cobweb Users', nominator_user, True),
            ('Cobweb Users', admin_user, True),

            ('Restricted', anon_user, False),
            ('Restricted', blacklisted_user, False),
            ('Restricted', random_user, False),
            ('Restricted', nominator_user, True),
            ('Restricted', admin_user, True),
        ):
            project.nomination_policy = nomination_policy
            assert project.is_nominator(user) == result, f'nomination_policy={nomination_policy}'


@pytest.mark.django_db
def test_nomination_model():
    nomination = NominationFactory()
    assert isinstance(nomination, Nomination)
    assert isinstance(str(nomination), str)


@pytest.mark.django_db
class TestClaimModel:

    def test_claim_creation(self):
        """Tests creation of Claim objects"""

        good_claim_data = {'nomination': NominationFactory(),
                           'organization': OrganizationFactory()}
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
        """Claim.is_admin(user) returns true for Claim's Project and Organization admins."""

        claim = ClaimFactory()
        assert claim.is_admin(AnonymousUser()) is False

        user = UserFactory()
        claim.nomination.project.nomination_policy = 'Cobweb Users'
        assert claim.is_admin(user) is True
        claim.nomination.project.nomination_policy = 'Restricted'
        assert claim.is_admin(user) is False

        claim.nomination.project.administrators.add(user)
        assert claim.is_admin(user) is True

        claim.nomination.project.administrators.remove(user)
        claim.organization.administrators.add(user)
        assert claim.is_admin(user) is True

        claim.nomination.project.administrators.add(user)
        assert claim.is_admin(user) is True
