import django_tables2
from django_tables2.utils import Accessor

from core.models import User, Organization, Resource


class CobwebBaseTable(django_tables2.Table):
    
    class Meta:
        abstract=True
        template_name = 'generic_table.html'
        attrs={'class': 'table table-hover'}
        order_by = ('-impact_factor', '-pk')
    
    def __init__(self, *args, table_title=None, new_item_link=None, **kwargs):
        self.table_title = table_title
        self.new_item_link = new_item_link
        super().__init__(*args, **kwargs)



class UserTable(CobwebBaseTable):

    class Meta(CobwebBaseTable.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name')
        empty_text = "No users."

    username = django_tables2.LinkColumn(
        viewname='user',
        kwargs={'username': Accessor('username')}
    )


class OrganizationTable(CobwebBaseTable):
    full_name = django_tables2.LinkColumn(viewname='organization_detail',
                                          verbose_name='Full name',
                                          kwargs={'pk': Accessor('pk')})

    class Meta(CobwebBaseTable.Meta):
        model = Organization
        fields = ('full_name', )
        empty_text = "No organizations."


class ResourceTable(CobwebBaseTable):
    title = django_tables2.LinkColumn(viewname='resource', kwargs={'url': Accessor('url')})
    url = django_tables2.LinkColumn(viewname='resource', kwargs={'url': Accessor('url')})

    class Meta(CobwebBaseTable.Meta):
        model = Resource
        fields = ('title', 'url')
        empty_text = "No records."
