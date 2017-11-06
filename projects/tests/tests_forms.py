from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from factory import DjangoModelFactory, Faker

from core.tests import UserFactory
from webresources.models import Resource
from webresources.tests import ResourceFactory

from projects import models, forms, tests, views
from projects.models import Project, Nomination



# class ProjectFormTests:

#     def test_init(self):
#         pass

# class NominationFormTests(TestCase):

#     def setUp(self):
#         self.nomination = tests.NominationFactory()

#         self.test_data = [
#             # ({test_data}, is_valid)
#             ({'wrong_field': 'wrong info'}, False),
#             ({'resource': 'twitter.com'}, True),
#             ({'resource': 'http://nytimes.com', 'Description': 'NYT'}, True),
#         ]

#     # def test_init_without_entry(self):
#     #     with self.assertRaises(KeyError):
#     #         forms.NominationForm()

#     def test_with_data(self):
#         for (data, valid) in self.test_data:
#             form = forms.NominationForm(data)
#             self.assertEqual(form.is_valid(), valid)

#     def test_nomination_form_links_to_resource(self):
#         form = forms.NominationForm({
#             'resource': 'http://twitter.com/',
#             'project': tests.ProjectFactory(),
#             'user': UserFactory(),
#             })
#         self.assertTrue(form.is_valid())
#         self.assertIsInstance(form.cleaned_data['resource'], Resource)

#     def test_nomination_form_normalizes_url(self):
#         form = forms.NominationForm({
#             'resource': 'twitter.com',
#             'project': tests.ProjectFactory(),
#             'user': UserFactory(),
#             })
#         self.assertTrue(form.is_valid())
#         self.assertEqual(form.cleaned_data['resource'], 
#             ResourceFactory(url="http://twitter.com"))