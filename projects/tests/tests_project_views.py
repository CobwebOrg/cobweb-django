from django.test import TestCase
from django.urls import reverse
import pytest

from core.tests.factories import UserFactory
from core.tests.factories import ResourceFactory

from projects.tests.factories import ProjectFactory, NominationFactory
from projects.models import Project


class TestProjectIndexView:

    @pytest.mark.xfail(strict=True)
    def test_project_table(self):
        """The table should be paginated correctly and include all projects."""
        # Fill the haystack index with projects

        # Test that all projects are listed and pagination works
        raise NotImplementedError

    @pytest.mark.django_db
    def test_new_project_link(self, client):
        """A 'new project' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        link_html = '<a href="/proj_create"'
        project_index_url = reverse('project_list')

        client.logout()
        assert link_html not in client.get(project_index_url).rendered_content

        client.force_login(UserFactory())
        assert link_html in client.get(project_index_url).rendered_content


class ProjectIndexViewTests(TestCase):

    def setUp(self):
        self.test_instances = [
            ProjectFactory(title="Boring Project"),
            ProjectFactory(title="Exciting Project"),
            ProjectFactory(title="Other Project"),
        ]
        self.response = self.client.get('/proj/')

    @pytest.mark.xfail(strict=True)
    def test_links_to_all_projects(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'generic_index.html')
        self.assertContains(self.response, 'Boring Project')
        self.assertContains(self.response, 'Exciting Project')
        self.assertContains(self.response, 'Other Project')


class ProjectDetailViewTests(TestCase):

    def setUp(self):
        self.test_instance = ProjectFactory()
        self.fields = ['title', 'description']
        self.templates = ['base.html', 'projects/project.html']

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
                nom.endorsements.add(UserFactory(username=username))

        self.client.logout()
        self.test_response = self.client.get(
            self.test_instance.get_absolute_url()
        )

    @pytest.mark.xfail(strict=True)
    def test_absolute_url_method(self):
        self.assertTrue(callable(self.test_instance.get_absolute_url))

    @pytest.mark.xfail(strict=True)
    def test_included_fields(self):
        for field in self.fields:
            self.assertContains(
                self.test_response,
                getattr(self.test_instance, field),
                html=True
            )

    @pytest.mark.xfail(strict=True)
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


    @pytest.mark.xfail(strict=True)
    def test_edit_project_link(self):
        """An 'edit project' link should be shown if logged-in user is
        authorized, otherwise hidden."""

        pass

    @pytest.mark.xfail(strict=True)
    def test_new_nomination_link(self):
        """A 'nominate' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        # OPEN NOMINATION POLICY

        self.test_instance.nomination_policy = 'Cobweb Users'
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


class TestProjectCreateView:

    @pytest.mark.django_db
    def test_anonymous_cant_create_project(self, client):
        client.logout()
        response = client.get(reverse('project_create'))
        assert (response.status_code==302 and 
                response.url=='/accounts/login/?next=/proj_create')

        project_data = {
            'title': 'Test Project for test_anonymous_cant_create_project',
            'status': 'Active',
            'nomination_policy': 'Cobweb Users',
        }

        response2 = client.post(reverse('project_create'), project_data)
        assert (response.status_code==302 and 
                response.url=='/accounts/login/?next=/proj_create')
        assert Project.objects.filter(title=project_data['title']).count() == 0

    @pytest.mark.xfail(strict=True)
    def test_user_creates_project(self):
        """...
        Should autmatically set: administrators"""
        raise NotImplementedError


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

    @pytest.mark.xfail(strict=True)
    def test_load(self):
        self.assertEqual(self.response.status_code, 200)
        for template in ['base.html', 'generic_form.html']:
            self.assertTemplateUsed(self.response, template)

    @pytest.mark.xfail(strict=True)
    def test_included_fields(self):
        for field_name in ['title', 'administrators', 'nomination_policy',
                           'nominators', 'status', 'description', 'tags']:
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

    @pytest.mark.xfail(strict=True)
    def test_no_edit_if_not_admin(self):
        """Anonymous and non-admin users get redirected to login page."""
        self.client.logout()
        self.assertRedirects(self.client.get(self.url),
                             f'/accounts/login/?next={self.url}')

        project_data = {
            'title': 'Test Project for test_anonymous_cant_create_project',
            'status': 'Active',
            'nomination_policy': 'Cobweb Users',
        }
        self.assertRedirects(self.client.post(self.url, project_data),
                             f'/accounts/login/?next={self.url}')

        self.client.force_login(UserFactory())
        self.assertRedirects(self.client.get(self.url),
                             f'/accounts/login/?next={self.url}')

        project_data = {
            'title': 'Test Project for test_anonymous_cant_create_project',
            'status': 'Active',
            'nomination_policy': 'Cobweb Users',
        }
        self.assertRedirects(self.client.post(self.url, project_data),
                             f'/accounts/login/?next={self.url}')
