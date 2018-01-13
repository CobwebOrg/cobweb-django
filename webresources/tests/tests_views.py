from django.test import TestCase
from django.urls import reverse
from faker import Faker

from archives.tests import HoldingFactory
from projects.tests import NominationFactory, ClaimFactory

from webresources import models, tests, views


class ResourceIndexViewTests(TestCase):

    def test_loads(self):
        response = self.client.get(reverse('webresources:list'))
        assert response.status_code == 200


class ResourceDetailViewTests(TestCase):

    def setUp(self):
        self.saved_resource = tests.ResourceFactory()
        self.saved_resource.save()
        self.saved_nomination = NominationFactory(resource=self.saved_resource)
        self.saved_nomination.save()
        self.saved_claim = ClaimFactory(nomination=self.saved_nomination)
        self.saved_claim.save()
        self.saved_holding = HoldingFactory(resource=self.saved_resource)
        self.saved_holding.save()
        self.url = self.saved_resource.url

    def test_get(self):
        """
        Tests that ResourceDetailView.get(...) performs URL normalization as
        follows:

        1. If url parameter is valid, or if called w/ id/pk instead of url,
        invoke super().get(...)

        2. If url is valid but non-cannonical (i.e. url ~= normalize_url(url) )
        then return a redirect using the cannonical url.

        3. If url is not valid, return a 404 or something [not implemented yet]

        Note that case #1 includes urls that are not yet in the database –
        custom logic for these cases in defined in .get_object(), which is
        invoked from the superclass's .get()
        """

        bad_url = 'https://www.twitter.com'
        good_url = models.normalize_url(bad_url)
        not_url = 'not a url'

        # # non-cannonical url should redirect
        bad_path = reverse('webresources:detail', kwargs={'url': bad_url})
        good_path = reverse('webresources:detail', kwargs={'url': good_url})
        self.assertRedirects(self.client.get(bad_path), good_path)

        # invalid url raises 404
        invalid_path = reverse('webresources:detail', kwargs={'url': not_url})
        self.assertEqual(self.client.get(invalid_path).status_code, 404)

    def test_get_object(self):
        """
        Tests that get_object(valid_url) always returns a Resource object.
        If such an object doesn't exist in the db yet, it will be created but
        not saved.

        This allows the ResourceDetailView to provide information such as
        parent/child resources, along with forms for nominating/claiming it
        (in which case the Resource should be saved along w/ Nomination or
        Claim object).
        """

        url = models.normalize_url(Faker().url())
        self.assertEqual(
            models.Resource.objects.filter(url__exact=url).count(), 0)
        new_resource = views.ResourceDetailView(
            kwargs={'url': url}).get_object()
        self.assertIsNone(new_resource.id)

        saved_resource = views.ResourceDetailView(
            kwargs={'url': self.url}).get_object()
        self.assertIsNotNone(saved_resource.id)
