import pytest
from django.test import TestCase
from django.urls import reverse
from lxml import html

from core.tests.factories import UserFactory
from webresources.tests.factories import ResourceFactory

from projects.tests.factories import ProjectFactory, NominationFactory, ClaimFactory
from projects.models import Project


class ProjectIndexViewTests(TestCase):

    def setUp(self):
        self.test_instances = [
            ProjectFactory(title="Boring Project"),
            ProjectFactory(title="Exciting Project"),
            ProjectFactory(title="Other Project"),
        ]
        self.response = self.client.get('/projects/')

    def test_links_to_all_projects(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'generic_index.html')
        self.assertTemplateUsed(self.response, 'generic_table.html')
        self.assertContains(self.response, 'Boring Project')
        self.assertContains(self.response, 'Exciting Project')
        self.assertContains(self.response, 'Other Project')

    def test_new_project_link(self):
        """A 'new project' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        link_html = """
            <a href="/projects/new" class="float-right btn btn-sm btn-primary">
                <strong>+</strong> New Project
            </a>
        """

        self.client.logout()
        self.assertNotContains(self.client.get('/projects/'), link_html, html=True)

        self.client.force_login(UserFactory())
        self.assertContains(self.client.get('/projects/'), link_html, html=True)


class ProjectDetailViewTests(TestCase):

    def setUp(self):
        self.test_instance = ProjectFactory()
        self.fields = ['title', 'description']
        self.templates = ['base.html', 'project.html']

        # Add some users
        self.admin_user = UserFactory()
        self.test_instance.administrators.add(self.admin_user)
        self.outside_user = UserFactory()
        self.nominator = UserFactory()
        self.test_instance.nominators.add(self.nominator)
        self.blacklisted_user = UserFactory()
        self.test_instance.nominator_blacklist.add(self.blacklisted_user)

        # Add some nominations
        self.user_nominations = {
            'facebook.com': ('user1', 'user3'),
            'linkedin.com': ('user2', 'user3'),
            'myspace.com': ('user3'),
            'twitter.com': ('user1', 'user2', 'user3'),
            'ucla.edu': ('user1', 'user3'),
        }
        for url, users in self.user_nominations.items():
            nom = NominationFactory(
                project=self.test_instance,
                resource=ResourceFactory(url=url),
            )
            for username in users:
                nom.nominated_by.add(UserFactory(username=username))

        self.client.logout()
        self.test_response = self.client.get(
            self.test_instance.get_absolute_url()
        )

    def test_absolute_url_method(self):
        self.assertTrue(callable(self.test_instance.get_absolute_url))

    def test_included_fields(self):
        for field in self.fields:
            self.assertContains(
                self.test_response,
                getattr(self.test_instance, field),
                html=True
            )

    def test_update_link(self):
        url = self.test_instance.get_absolute_url()
        edit_link = f'<a href="{self.test_instance.get_edit_url()}">'

        # admin user -> link
        self.client.force_login(self.admin_user)
        self.assertContains(self.client.get(url), edit_link)

        # nominator -> no link
        self.client.force_login(self.nominator)
        self.assertNotContains(self.client.get(url), edit_link, html=True)

        # other user -> no link
        self.client.force_login(self.outside_user)
        self.assertNotContains(self.client.get(url), edit_link, html=True)

        # anonymous user -> no link
        self.client.logout()
        self.assertNotContains(self.client.get(url), edit_link, html=True)


    def test_edit_project_link(self):
        """An 'edit project' link should be shown if logged-in user is
        authorized, otherwise hidden."""

        pass

    def test_new_nomination_link(self):
        """A 'nominate' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        # ANONYMOUS NOMINATION POLICY

        self.test_instance.nomination_policy = 'Anonymous'
        self.test_instance.save()

        # Anonymous User
        self.client.logout()
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.outside_user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.admin_user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.nominator)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.blacklisted_user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertNotContains(response, 'Add a nomination')
        self.assertNotContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        # OPEN NOMINATION POLICY

        self.test_instance.nomination_policy = 'Open'
        self.test_instance.save()

        # Anonymous User
        self.client.logout()
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertNotContains(response, 'Add a nomination')
        self.assertNotContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.outside_user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.admin_user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.nominator)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.blacklisted_user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertNotContains(response, 'Add a nomination')
        self.assertNotContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        # RESTRICTED NOMINATION POLICY

        self.test_instance.nomination_policy = 'Restricted'
        self.test_instance.save()

        # Anonymous User
        self.client.logout()
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertNotContains(response, 'Add a nomination')
        self.assertNotContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.outside_user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertNotContains(response, 'Add a nomination')
        self.assertNotContains(
            response,
            reverse('nominate',  kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.admin_user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.nominator)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )

        self.client.force_login(self.blacklisted_user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertNotContains(response, 'Add a nomination')
        self.assertNotContains(
            response,
            reverse('nominate', kwargs={'project_id': self.test_instance.pk})
        )


class ProjectCreateViewTests(TestCase):

    def test_anonymous_cant_create_project(self):
        self.client.logout()
        response = self.client.get(reverse('project_create'))
        self.assertRedirects(response, '/accounts/login/?next=/projects/new')

        project_data = {
            'title': 'Test Project for test_anonymous_cant_create_project',
            'status': 'Active',
            'nomination_policy': 'Open',
        }

        response2 = self.client.post(reverse('project_create'), project_data)
        self.assertRedirects(response2, '/accounts/login/?next=/projects/new')
        assert Project.objects.filter(title=project_data['title']).count() == 0

    def test_user_creates_project(self):
        """...
        Should autmatically set: administrators"""
        pass


class ProjectUpdateViewTests(TestCase):

    def setUp(self):
        self.project = ProjectFactory()
        self.project.save()

        # make some users
        self.admin_user = UserFactory()
        self.project.administrators.add(self.admin_user)

        # get a default response
        self.url = self.project.get_edit_url()
        self.client.force_login(self.admin_user)
        self.response = self.client.get(self.url)

    def test_load(self):
        self.assertEqual(self.response.status_code, 200)
        for template in ['base.html', 'generic_form.html']:
            self.assertTemplateUsed(self.response, template)

    def test_included_fields(self):
        for field_name in ['title', 'administrators', 'nomination_policy',
                           'nominators', 'status', 'description', 'keywords']:
            try:
                self.assertContains(
                    self.response,
                    f'id="id_{field_name}"',
                    html=False
                )
            except AssertionError:
                self.assertContains(
                    self.response,
                    f'id="div_id_{field_name}"',
                    html=False
                )

    def test_no_edit_if_not_admin(self):
        """Anonymous and non-admin users get redirected to login page."""
        self.client.logout()
        self.assertRedirects(self.client.get(self.url),
                             f'/accounts/login/?next={self.url}')

        project_data = {
            'title': 'Test Project for test_anonymous_cant_create_project',
            'status': 'Active',
            'nomination_policy': 'Open',
        }
        self.assertRedirects(self.client.post(self.url, project_data),
                             f'/accounts/login/?next={self.url}')

        self.client.force_login(UserFactory())
        self.assertRedirects(self.client.get(self.url),
                             f'/accounts/login/?next={self.url}')

        project_data = {
            'title': 'Test Project for test_anonymous_cant_create_project',
            'status': 'Active',
            'nomination_policy': 'Open',
        }
        self.assertRedirects(self.client.post(self.url, project_data),
                             f'/accounts/login/?next={self.url}')


@pytest.mark.django_db
class TestNominationDetailView:

    def test_loads(self, client):
        response = client.get(NominationFactory().get_absolute_url())
        assert response.status_code == 200

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