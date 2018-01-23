from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone
import pytest

from archives.tests import CollectionFactory
from projects.models import Project, Nomination, Claim
from projects.tests import ProjectFactory, NominationFactory, ClaimFactory


class ProjectModelTests(TestCase):

    def setUp(self):
        self.test_instance = ProjectFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Project)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)

    def test_is_nominator_function(self):
        pass


class NominationModelTests(TestCase):

    def setUp(self):
        self.test_instance = NominationFactory()

    def test_creation(self):
        self.assertIsInstance(self.test_instance, Nomination)

    def test_str(self):
        """Tests that str(object) always returns a str."""
        self.assertIsInstance(str(self.test_instance), str)


@pytest.mark.django_db
class ClaimModelTests:

    def test_claim_creation():
        """Tests creation of Claim objects"""

        good_claim_data = {'nomination': NominationFactory(),
                           'collection': CollectionFactory(),
                           'start_date': timezone.now()}
        Claim.objects.create(**good_claim_data).save()

        # Duplicate data should raise error
        with pytest.raises(IntegrityError):
            Claim.objects.create(**good_claim_data)

    def test_create_with_incomplete_data():
        incomplete_data = {'nomination': NominationFactory()}
        with pytest.raises(IntegrityError):
            Claim.objects.create(**incomplete_data)

    def test_str():
        """Tests that str(object) always returns a str."""
        assert isinstance(str(NominationFactory), str)

    def test_Claim_get_resource_set():
        """.get_resource_set() should return a collection object."""

        collection = CollectionFactory()
        assert ClaimFactory(collection=collection).get_resource_set() == collection
