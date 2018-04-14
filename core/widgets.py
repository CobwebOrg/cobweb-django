from django.forms.widgets import URLInput

from core.models import Resource

class ResourceInput(URLInput):
    """
    URLInput for Resource objects.
    """

    def format_value(self, value):
        """
        Return a value as it should appear when rendered in a template.

        Currently, value might be an int, the primary key to a Resource object.
        format_value looks up that Resource and returns its URL. This is dumb
        and convoluted, and I should just store the URL directly in each
        Nomination or Claim.
        """
        if isinstance(value, int):
            return Resource.objects.get(id=value).url
        else:
            return value
