from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView
import django_tables2
from django_tables2.utils import Accessor
from reversion.views import RevisionMixin

from archives import models
from archives.forms import CollectionForm

class CollectionTable(django_tables2.Table):

    title = django_tables2.LinkColumn()
    nholdings = django_tables2.TemplateColumn(
        '{% load collection_count_badge from cobweb_look %}'
        '{% collection_count_badge record %}',
        default='', orderable=False
    )

    class Meta:
        model = models.Collection
        show_header = False
        fields = ['title', 'nholdings']
        # attrs = {'class': 'table table-hover'}
        empty_text = "No collections."


class HoldingTable(django_tables2.Table):

    resource = django_tables2.LinkColumn(
        'resource_detail',
        kwargs={'url': Accessor('resource.url')}
    )
    tags = django_tables2.TemplateColumn(
        """
        {% load badge from cobweb_look %}
        <small>
            {% for tag in record.tags.all %}
                {% badge tag %}
            {% endfor %}
        </small>
        """, default='', orderable=False
    )

    class Meta:
        model = models.Holding
        show_header = False
        fields = ['resource', 'tags']
        empty_text = "No records."


class CollectionIndexView(django_tables2.SingleTableView):
    model = models.Collection
    template_name = "generic_index.html"
    table_class = CollectionTable
    section = 'collection'


class CollectionDetailView(django_tables2.SingleTableMixin, DetailView):
    model = models.Collection
    template_name = "archives/collection.html"
    table_class = HoldingTable
    section = 'collection'

    def get_table_data(self):
        return self.object.holdings.all()

class CollectionUpdateView(UserPassesTestMixin, RevisionMixin, UpdateView):
    model = models.Collection
    template_name = 'generic_form.html'
    form_class = CollectionForm
    section = 'collection'

    def test_func(self):
        admins = self.get_object().administrators.all()
        ans = self.request.user in admins or admins.count()==0
        return ans


class CollectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return get_user_model().objects.none()

        qs = models.Collection.objects.all()

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        return qs
