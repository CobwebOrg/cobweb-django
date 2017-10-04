import ajax_select
from django.db.models import Q

from metadata.models import MDProperty

@ajax_select.register('md_property')
class MDPropertyLookup(ajax_select.LookupChannel):

    model = MDProperty
    min_length = 1

    def get_query(self, q, request):
        return self.model.objects.filter(
              Q(name__icontains=q) 
            | Q(vocabulary__name__icontains=q)
        ).distinct()

    def format_item_display(self, item):
        html = ''
        if item.vocabulary:
            html = "<span class='md_vocabulary badge badge-pill badge-info'>{}</span>".format(
                item.vocabulary)
        if item.name:
            html = "<span class='md_term badge badge-pill badge-light'>{} {}</span>".format(
                html, item.name)
        return html

    def format_match(self, item):
        return self.format_item_display(item)