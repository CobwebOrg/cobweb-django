from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from factory import DjangoModelFactory, Faker

from core.tests import AgentFactory
from webresources.models import Resource
from webresources.tests import ResourceFactory

from projects import models, forms, views
from projects.models import Project, Nomination


class FormTestsMixin:

    def test_init(self):
        self.form_class()

    # def test_init_without_entry(self):
    #     with self.assertRaises(KeyError):
    #         self.form_class()

    def test_with_data(self):
        for (data, valid) in self.test_data:
            form = self.form_class(data)
            self.assertEqual(form.is_valid(), valid)


class NominationFormTests(FormTestsMixin, TestCase):

    def setUp(self):
        self.test_object = get_nomination()
        self.form_class = forms.NominationForm

        self.test_data = [
            # ({test_data}, is_valid)
            ({'wrong_field': 'wrong info'}, False),
            ({'resource': 'twitter.com'}, True),
            ({'resource': 'http://nytimes.com', 'Description': 'NYT'}, True),
        ]

    def test_nomination_form_links_to_resource(self):
        form = forms.NominationForm({
            'resource': 'http://twitter.com',
            'project': get_project(),
            'user': get_user(),
            })
        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.cleaned_data['resource'], Resource)

    def test_nomination_form_normalizes_url(self):
        form = forms.NominationForm({
            'resource': 'twitter.com',
            'project': get_project(),
            'user': get_user(),
            })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['resource'], get_resource(location="http://twitter.com"))