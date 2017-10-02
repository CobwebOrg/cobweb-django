
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core import forms
from core.models import Organization

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Organization
from core.tests import UserFactory, OrganizationFactory


class ViewTestsMixin:

    def test_load(self):
        self.assertEqual(self.test_response.status_code, 200)
        for template in self.templates:
            self.assertTemplateUsed(self.test_response, template)

class IndexViewTestsMixin(ViewTestsMixin):

    def test_list(self):
        """Index Views should list  *all* instances of a class
        (This test will have to change when we introduce pagination.)"""
        for instance in self.test_instances:
            import ipdb; ipdb.set_trace()
            self.assertContains(self.test_response, str(instance))
            self.assertContains(self.test_response, instance.get_absolute_url())

class DetailViewTestsMixin(ViewTestsMixin):

    def test_absolute_url_method(self):
        self.assertTrue(callable(self.test_instance.get_absolute_url))

    def test_included_fields(self):
        for field in self.fields:
            self.assertContains(self.test_response, getattr(self.test_instance, field), html=True)

    def test_update_link(self):
        pass

class HomePageTests(TestCase):

    def test_homepage(self):
        """Root URL '/' should return HTTP status 200 (i.e. success)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class ProjectListViewTests(TestCase):

    def setUp(self):
        self.test_instances = [ ProjectFactory() for n in range(3) ]
        self.test_response = self.client.get(reverse('project_list'))

    def test_load(self):
        self.assertEqual(self.test_response.status_code, 200)

    def test_templates(self):
        self.assertTemplateUsed(self.test_response, 'base.html')
        self.assertTemplateUsed(self.test_response, 'project_list.html')

class UserIndexViewTests(IndexViewTestsMixin, TestCase):

    def setUp(self):
        self.test_instances = [ UserFactory() for n in range(3) ]
        self.templates = [ 'base.html', 'user_list.html' ]
        self.test_response = self.client.get(reverse('user_list'))

class UserDetailViewTests(DetailViewTestsMixin, TestCase):

    def setUp(self):
        self.test_instance = get_user()
        self.fields = [ 'username' ]
        self.templates = [ 'base.html', 'user_detail.html' ]
        self.test_response = self.client.get(self.test_instance.get_absolute_url())

class UserCreateViewTests(TestCase):

    def setUp(self):
        pass

    def test_user_create_view_fields(self):
        pass

class UserUpdateViewTests(TestCase):

    def setUp(self):
        pass

    def test_user_update_view_fields(self):
        pass
