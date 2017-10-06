import ajax_select
from django.db.models import Q

from django.contrib.auth import get_user_model

@ajax_select.register('users')
class UserLookup(ajax_select.LookupChannel):

    model = get_user_model()
    min_length = 3

    def get_query(self, q, request):
        return self.model.objects.filter(
              Q(username__icontains=q) 
            | Q(first_name__icontains=q) 
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
        ).distinct()

    def format_item_display(self, item):
        return "<span class='user'>{}</span>".format(str(item))

    def can_add(user, other_model):
        return False