import django_tables2
from django_tables2.utils import Accessor

from core.models import User, Organization, Resource


class UserTable(django_tables2.Table):
    username = django_tables2.LinkColumn(viewname='user_detail', kwargs={'pk': Accessor('pk')})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        attrs={'class': 'table table-hover'}
        empty_text = "No users."
        order_by = ('-impact_factor', '-pk')


class OrganizationTable(django_tables2.Table):
    name = django_tables2.LinkColumn(viewname='organization_detail', kwargs={'pk': Accessor('pk')})

    class Meta:
        model = Organization
        fields = ('name', )
        attrs={'class': 'table table-hover'}
        empty_text = "No organizations."
        order_by = ('-impact_factor', '-pk')


class ResourceTable(django_tables2.Table):
    url = django_tables2.LinkColumn(viewname='resource_detail', kwargs={'pk': Accessor('pk')})

    class Meta:
        model = Resource
        fields = ('url', )
        attrs={'class': 'table table-hover'}
        empty_text = "No records."
        order_by = ('-impact_factor', '-pk')


class OldResourceTable(django_tables2.Table):

    url = django_tables2.LinkColumn()
    nominations = django_tables2.TemplateColumn(
        '{% load count_badge from cobweb_look %}'
        '{% count_badge record.nominations %}',
        default='', orderable=False
    )
    holdings = django_tables2.TemplateColumn(
        '{% load count_badge from cobweb_look %}'
        '{% count_badge record.holdings %}',
        default='', orderable=False
    )

    class Meta:
        model = Resource
        show_header = False
        exclude = ['id']
        empty_text = "No records."