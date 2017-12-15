from django.views.generic import ListView, DetailView
import django_tables2

from archives import models


class CollectionTable(django_tables2.Table):

    title = django_tables2.LinkColumn()
    h = django_tables2.TemplateColumn('{% load icon from cobweb_look %}' +
                                      '{{record.holdings.count}}' +
                                      '{% icon "Holding" %}',
                                      orderable=False)

    class Meta:
        model = models.Collection
        show_header = True
        fields = ['title', 'h']
        attrs = {'class': 'table table-hover'}
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
    template_name = "archives/collection_list.html"
    table_class = CollectionTable


class CollectionDetailView(django_tables2.SingleTableMixin, DetailView):
    model = models.Collection
    template_name = "archives/collection.html"
    table_class = HoldingTable

    def get_table_data(self):
        # print(dir(self))
        return self.object.holdings.all()