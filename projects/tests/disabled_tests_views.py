from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from factory import DjangoModelFactory, Faker

from core.tests import AgentFactory
from webresources.models import Resource
from webresources.tests import ResourceFactory

from projects import models, forms, views
from projects.models import Project, Nomination


class DetailViewTestsMixin(ViewTestsMixin):

    def test_absolute_url_method(self):
        self.assertTrue(callable(self.test_instance.get_absolute_url))

    def test_included_fields(self):
        for field in self.fields:
            self.assertContains(self.test_response, getattr(self.test_instance, field), html=True)

    def test_update_link(self):
        pass

class ProjectIndexViewTests(TestCase):
    
    def setUp(self):
        get_project(name="Boring Project")
        get_project(name="Exciting Project")
        get_project(name="Other Project")
        self.response = self.client.get('/projects/')

    def test_links_to_all_projects(self):
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'project_list.html')
        self.assertContains(self.response, 'Boring Project')
        self.assertContains(self.response, 'Exciting Project')
        self.assertContains(self.response, 'Other Project')

    def test_new_project_link(self):
        """A 'new project' link should be shown if logged-in user is authorized,
        otherwise hidden."""
        self.client.logout()
        self.assertNotContains(self.client.get('/projects/'), 'Create new project')
        self.assertNotContains(self.client.get('/projects/'), reverse('project_create'))
        self.client.force_login(get_user())
        self.assertContains(self.client.get('/projects/'), 'Create new project')
        self.assertContains(self.client.get('/projects/'), reverse('project_create'))

class ProjectDetailViewTests(DetailViewTestsMixin, TestCase):

    def setUp(self):
        self.test_instance = get_project(description = "Just a test project.")
        self.fields = [ 'name', 'description' ]
        self.templates = [ 'base.html', 'project_detail.html' ]

        # Add some nominations
        self.user_nominations = {
            'facebook.com': ('user1', 'user3'),
            'linkedin.com': ('user2', 'user3'),
            'myspace.com': ('user3'),
            'twitter.com': ('user1', 'user2', 'user3'),
            'ucla.edu': ('user1', 'user3'),
        }
        for url, users in self.user_nominations.items():
            for username in users:
                get_nomination(
                    project=self.test_instance,
                    nominated_by=get_agent(user=get_user(username=username)),
                    resource=get_resource(location=url),
                )


        self.client.logout()
        self.test_response = self.client.get(self.test_instance.get_absolute_url())

    def test_each_nominated_resource_listed_only_once(self):
        """Each nominated resource should be listed on the Project Detail page.
        If it was nominated by multiple users, it should appear only once.

        As currently written, this test will also fail if the resource url is 
        included in a link, which shouldn't happen."""
        
        for url, users in self.user_nominations.items():
            self.assertContains(self.test_response, url, count=1)

    def test_edit_project_link(self):
        """An 'edit project' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        pass

    def test_new_nomination_link(self):
        """A 'nominate' link should be shown if logged-in user is authorized,
        otherwise hidden."""

        self.client.logout()
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertNotContains(response, 'Add a nomination')
        self.assertNotContains(response, reverse('nominate', kwargs={'project_id': self.test_instance.pk}))

        self.client.force_login(self.test_instance.administered_by.objects.get.user)
        response = self.client.get(self.test_instance.get_absolute_url())
        self.assertContains(response, 'Add a nomination')
        self.assertContains(response, reverse('nominate', kwargs={'project_id': self.test_instance.pk}))

    def test_username_not_agent_str(self):
        """'Created by' lists string representation of User, not Agent."""
        self.assertContains(
            self.test_response, 
            self.test_instance.established_by.user.get_full_name()
        )
        self.assertNotContains(
            self.test_response, 
            str(self.test_instance.established_by)
        )

class ProjectCreateViewTests(TestCase):

    def setUp(self):
        pass

    def test_anonymous_cant_create_project(self):
        pass

    def test_user_creates_project(self):
        """...
        Should autmatically set: User"""
        pass

class NominationCreateViewTests(TestCase):

    def setUp(self):
        pass

    def test_anonymous_cannot_nominate_to_restricted_project(self):
        pass

    def test_user_creates_project(self):
        """...
        Should autmatically set: User"""
        pass
      
