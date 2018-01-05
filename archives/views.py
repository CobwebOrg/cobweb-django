from django.views.generic import ListView, DetailView
import django_tables2

from archives import models


class CollectionTable(django_tables2.Table):

    title = django_tables2.LinkColumn()
    nholdings = django_tables2.TemplateColumn(
        '{% load resource_count_badge from cobweb_look %}'
        '{% resource_count_badge record %}',
        default='', orderable=False
    )

    class Meta:
        model = models.Collection
        show_header = False
        fields = ['title', 'nholdings']
        # attrs = {'class': 'table table-hover'}
        empty_text = "No collections."


class HoldingTable(django_tables2.Table):

    title = django_tables2.LinkColumn()

    class Meta:
        model = models.Holding
        show_header = True
        fields = ['title', 'resource']
        attrs = {'class': 'table table-hover'}
        empty_text = "No records."


class CollectionIndexView(django_tables2.SingleTableView):
    model = models.Collection
    template_name = "generic_index.html"
    table_class = CollectionTable


class CollectionDetailView(django_tables2.SingleTableMixin, DetailView):
    model = models.Collection
    template_name = "archives/collection.html"
    table_class = HoldingTable

    def get_table_data(self):
        # print(dir(self))
        return self.object.holdings.all()
