import ajax_select
from django.db.models import Q

from metadata.models import Keyword

@ajax_select.register('keywords')
class KeywordLookup(ajax_select.LookupChannel):

    model = Keyword
    min_length = 1

    def get_query(self, q, request):
        return self.model.objects.filter(name__icontains=q)

    def format_item_display(self, item):
        return "<span class='badge badge-pill badge-info'>{}</span>".format(
                item.name)

    def format_match(self, item):
        return self.format_item_display(item)

    def can_add(user, other_model):
        return True