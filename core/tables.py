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
    class Meta(CobwebBaseTable.Meta):
        model = Organization
        fields = ('name', 'n_claimed', 'n_held')
        empty_text = "No organizations."

    name = django_tables2.LinkColumn(verbose_name='Full name',
                                     viewname='organization',
                                     kwargs={'slug': Accessor('object.slug')})

    n_claimed = django_tables2.Column(
        verbose_name='Claimed',
        attrs={'cell': {'class': 'text-center'}},
    )
    n_held = django_tables2.Column(
        verbose_name='Held',
        attrs={'cell': {'class': 'text-center'}},
    )

    def render_claimed_nominations(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="badge-claimed">{}</span>', value)

    def render_held_nominations(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="badge-held">{}</span>', value)


class ResourceTable(CobwebBaseTable):
    title = django_tables2.LinkColumn(viewname='resource', kwargs={'url': Accessor('url')})
    url = django_tables2.LinkColumn(viewname='resource', kwargs={'url': Accessor('url')})

    class Meta(CobwebBaseTable.Meta):
        model = Resource
        fields = ('title', 'url')
        empty_text = "No records."
