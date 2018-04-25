from django.test import TestCase

from core.models import User
from core.templatetags import cobweb_look


class IconTagTests(TestCase):
    """{% icon [x] %} returns icon HTML, for specified x."""

    def test_strings(self):
        """{% icon [x] %} works for certain strings."""
        assert (cobweb_look.icon('User')
                == '<span title="User" class="fas fa-user"></span>')
        assert (cobweb_look.icon('edit')
                == '<span title="edit" class="fas fa-edit"></span>')

    def test_objects(self):
        """{% icon [x] %} works for certain objects."""
        assert (cobweb_look.icon(User)
                == '<span title="User" class="fas fa-user"></span>')
