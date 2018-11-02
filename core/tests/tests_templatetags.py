import pytest
from haystack.query import SearchQuerySet

from core.models import Organization
from core.templatetags import cobweb_look
from core.tests.factories import OrganizationFactory

@pytest.mark.django_db
def test_model():
    org = OrganizationFactory()
    assert cobweb_look.model(Organization) is Organization
    assert cobweb_look.model(org) is Organization
    # assert cobweb_look.model(
    #     SearchQuerySet().filter(django_ct='core.organization').best_match()
    # ) is Organization
