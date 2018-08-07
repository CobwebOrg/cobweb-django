import pytest
from django.db.utils import IntegrityError

from core.models import User, Organization
from core.models import Note, Tag, SubjectHeading
from core.models import Resource, ResourceDescription, ResourceScan
from core.tests.factories import UserFactory, OrganizationFactory
from core.tests.factories import NoteFactory, TagFactory, SubjectHeadingFactory
from core.tests.factories import ResourceFactory, ResourceScanFactory, ResourceDescriptionFactory


@pytest.mark.django_db
def test_user_model():
    user = UserFactory()
    assert isinstance(user, User)
    assert isinstance(str(user), str)


@pytest.mark.django_db
def test_organization_model():
    org = OrganizationFactory()
    assert isinstance(org, Organization)
    assert isinstance(str(org), str)


@pytest.mark.django_db
def test_note_model():
    note = NoteFactory()
    assert isinstance(note, Note)
    assert isinstance(str(note), str)


@pytest.mark.django_db
def test_tag_model():
    tag = TagFactory()
    assert isinstance(tag, Tag)
    assert isinstance(str(tag), str)


@pytest.mark.django_db
def test_subjectheading_model():
    subject_heading = SubjectHeadingFactory()
    assert isinstance(subject_heading, SubjectHeading)
    assert isinstance(str(subject_heading), str)


@pytest.mark.django_db
def test_resource_model():
    resource = ResourceFactory()
    assert isinstance(resource, Resource)
    assert isinstance(str(resource), str)
    with pytest.raises(IntegrityError):
        str(ResourceFactory(url=None))


class TestResourceScanModel:

    @pytest.mark.django_db
    def test_creation(self):
        resource_scan = ResourceScanFactory()
        assert isinstance(resource_scan, ResourceScan)
        assert isinstance(str(resource_scan), str)


@pytest.mark.django_db
def test_resource_description_model():
    resource_description = ResourceDescriptionFactory()
    assert isinstance(resource_description, ResourceDescription)
    assert isinstance(str(resource_description), str)
