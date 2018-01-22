import pytest
from django.test import TestCase
from django.urls import reverse

from archives import tests
from archives.tests import CollectionFactory
from core.tests import UserFactory


class CollectionIndexViewTests(TestCase):

    def setUp(self):
        self.test_instances = [
            tests.CollectionFactory(title="Boring Collection"),
            tests.CollectionFactory(title="Exciting Collection"),
            tests.CollectionFactory(title="Other Collection"),
        ]
        self.response = self.client.get('/collections/')

    def test_loads(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'generic_index.html')
        self.assertTemplateUsed(self.response, 'generic_table.html')

    def test_title(self):
        self.assertContains(self.response, '<h3>Collections',
                            count=1, html=True)

    def test_links_to_all_collections(self):
        self.assertContains(self.response, 'Boring Collection')
        self.assertContains(self.response, 'Exciting Collection')
        self.assertContains(self.response, 'Other Collection')


class CollectionDetailViewTests(TestCase):

    def setUp(self):
        self.test_instance = tests.CollectionFactory()
        self.test_instance.metadata = {'a': [1], 'b': [2, 3], 'c': ['hello']}
        self.test_instance.save()

        self.client.logout()
        self.response = self.client.get(
            self.test_instance.get_absolute_url()
        )

    def test_loads(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'base.html')
        self.assertTemplateUsed(self.response, 'archives/collection.html')

    def test_absolute_url_method(self):
        self.assertTrue(callable(self.test_instance.get_absolute_url))

    @pytest.mark.xfail(strict=True)
    def test_included_fields(self):
        for field in ('title', 'description'):
            self.assertContains(
                self.response,
                getattr(self.test_instance, field),
                html=True
            )
        for k, vs in self.test_instance.metadata.items():
            self.assertContains(self.response, k.capitalize() + ':', html=True)
            for v in vs:
                try:
                    self.assertContains(self.response, str(v), html=True)
                except AssertionError:
                    self.assertIn(str(v), self.response.rendered_content)

    @pytest.mark.xfail(strict=True)
    def test_claim_orphan_link(self):
        claim_orphan_url = reverse('archives:claim',
                                   kwargs={'pk': self.test_instance.id})
        claim_orphan_html = f'<a href="{claim_orphan_url}"'
        self.assertContains(self.response, claim_orphan_html)


# class CollectionCreateViewTests(TestCase):

#     def setUp(self):
#         pass

#     def test_anonymous_cant_create_collection(self):
#         pass

#     def test_user_creates_collection(self):
#         """...
#         Should automatically set: User"""
#         pass


class CollectionUpdateViewTests(TestCase):

    def setUp(self):
        user = UserFactory()
        self.collection = CollectionFactory()
        self.collection.save()
        self.collection.administrators.add(user)
        self.client.force_login(user)
        self.response = self.client.get(self.collection.get_edit_url())

    def test_load(self):
        self.assertEqual(self.response.status_code, 200)
        for template in ['base.html', 'generic_form.html']:
            self.assertTemplateUsed(self.response, template)

#     def test_included_fields(self):
#         for field_name in ['title', 'administrators', 'nomination_policy',
#                            'nominators', 'status', 'description', 'keywords']:
#             try:
#                 self.assertContains(
#                     self.response,
#                     f'id="id_{field_name}"',
#                     html=False
#                 )
#             except AssertionError:
#                 self.assertContains(
#                     self.response,
#                     f'id="div_id_{field_name}"',
#                     html=False
#                 )

#     def test_permissions_to_edit_collection(self):
#         pass
