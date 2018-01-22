from dal.autocomplete import ModelSelect2Multiple
from django.test import TestCase

from projects import forms
from projects.tests import NominationFactory


class ProjectFormTests(TestCase):

    def test_multiselect_widgets(self):
        form = forms.ProjectForm()
        self.assertIsInstance(form, forms.ProjectForm)
        for field in ('administrators', 'nominators', 'keywords'):
            self.assertIsInstance(
                form.fields[field].widget,
                ModelSelect2Multiple
            )

#     def test_init(self):
#         pass

class NominationFormTests(TestCase):

    def test_init_without_entry(self):
        form = forms.NominationForm()
        assert form.is_valid() == False

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
