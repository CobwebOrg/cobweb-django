import pytest
from haystack.query import SearchQuerySet

from core.models import User
from core.templatetags import cobweb_look
from core.tests.factories import UserFactory

@pytest.mark.django_db
def test_model():
    assert cobweb_look.model(User) is User
    assert cobweb_look.model(UserFactory()) is User
    assert cobweb_look.model(
        SearchQuerySet().filter(django_ct='core.user').best_match()
    ) is User
