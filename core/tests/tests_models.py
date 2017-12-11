from django.contrib.auth import get_user_model
from django.test import TestCase

from projects.tests import ProjectFactory

from core.models import Organization
from core.tests import UserFactory, OrganizationFactory


class UserModelTests(TestCase):

    def setUp(self):
        self.test_instance = UserFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, get_user_model())

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

        # # Make sure it works even if the usual fields are blank
        # try:
        #     self.assertIsInstance(
        #         str(UserFactory(first_name=None, last_name=None,
        #                         username=None)),
        #         str,
        #     )
        # except:
        #     pass

    def test_get_projects_and_collections(self):
        """Tests that User.get_projects_and_collections() returns the set of
        Projects the user can nominate to and (in future, not yet implemented)
        Collections they can claim on behalf of."""

        anonymous_project = ProjectFactory(nomination_policy='A',
                                           title='anonymous_project')
        anonymous_project.save()

        open_project = ProjectFactory(nomination_policy='O',
                                      title='open_project')
        open_project.save()

        admin_project = ProjectFactory(nomination_policy='R',
                                       title='admin_project')
        admin_project.save()
        admin_project.administered_by.add(self.test_instance)

        nominator_project = ProjectFactory(nomination_policy='R',
                                           title='nominator_project')
        nominator_project.save()
        nominator_project.nominators.add(self.test_instance)

        included_projects = [
            anonymous_project,
            open_project,
            admin_project,
            nominator_project,
        ]

        not_nominator_project = ProjectFactory(nomination_policy='R',
                                               title='not_nominator_project')
        not_nominator_project.save()

        blacklisted_project = ProjectFactory(nomination_policy='O',
                                             title='blacklisted_project')
        blacklisted_project.save()
        blacklisted_project.nominator_blacklist.add(self.test_instance)

        excluded_projects = [
            not_nominator_project,
            blacklisted_project,
        ]

        queryset = self.test_instance.get_projects_and_collections()

        # import ipdb; ipdb.set_trace()
        for project in included_projects:
            self.assertIn(project, queryset)

        for project in excluded_projects:
            self.assertNotIn(project, queryset)


class OrganizationModelTests(TestCase):

    def setUp(self):
        self.test_instance = OrganizationFactory()

    def test_organization_creation(self):
        """Tests creation of Organization objects"""

        self.assertIsInstance(self.test_instance, Organization)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

        # # Make sure it works even if the usual fields are blank
        # try:
        #     self.assertIsInstance(
        #         str(OrganizationFactory(title=None, identifier=None)),
        #         str,
        #     )
        # except:
        #     pass
