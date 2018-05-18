import django_tables2
from django_tables2.utils import Accessor

from core.models import User, Organization, Resource


class CobwebBaseTable(django_tables2.Table):

    class Meta:
        abstract=True
        attrs={'class': 'table table-hover'}
        order_by = ('-impact_factor', '-pk')



class UserTable(CobwebBaseTable):
    username = django_tables2.LinkColumn(viewname='user_detail', kwargs={'pk': Accessor('pk')})

    class Meta(CobwebBaseTable.Meta):
        model = User
        fields = ('impact_factor', 'username', 'first_name', 'last_name')
        empty_text = "No users."


class OrganizationTable(CobwebBaseTable):
    full_name = django_tables2.LinkColumn(viewname='organization_detail', kwargs={'pk': Accessor('pk')})

    class Meta(CobwebBaseTable.Meta):
        model = Organization
        fields = ('impact_factor', 'full_name', )
        empty_text = "No organizations."


class ResourceTable(CobwebBaseTable):
    url = django_tables2.LinkColumn(viewname='resource_detail', kwargs={'url': Accessor('url')})

    class Meta(CobwebBaseTable.Meta):
        model = Resource
        fields = ('impact_factor', 'title', 'url')
        empty_text = "No records."
