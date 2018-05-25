from django.utils.html import format_html
import django_tables2
from django_tables2.utils import Accessor

from core.tables import CobwebBaseTable
from projects.models import Project, Nomination, Claim


class ProjectTable(CobwebBaseTable):
    """django_tables2.Table object for lists of projects."""

    class Meta(CobwebBaseTable.Meta):
        model = Project
        fields = ('title', 'unclaimed_nominations',
                  'claimed_nominations', 'held_nominations')
        empty_text = "No projects."

    title = django_tables2.LinkColumn(
        viewname='project_summary',
        kwargs={'pk': Accessor('pk')},
    )
    unclaimed_nominations = django_tables2.Column(
        verbose_name='Unclaimed',
        attrs={'cell': {'class': 'text-center'}},
    )
    claimed_nominations = django_tables2.Column(
        verbose_name='Claimed',
        attrs={'cell': {'class': 'text-center'}},
    )
    held_nominations = django_tables2.Column(
        verbose_name='Held',
        attrs={'cell': {'class': 'text-center'}},
    )

    def render_unclaimed_nominations(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="badge-unclaimed">{}</span>',
                               value)

    def render_claimed_nominations(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="badge-claimed">{}</span>',
                               value)

    def render_held_nominations(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="badge-held">{}</span>',
                               value)
    

class NominationTable(CobwebBaseTable):
    """django_tables2.Table object for lists of nominations."""

    class Meta(CobwebBaseTable.Meta):
        model = Nomination
        fields = ('url', 'status', 'claim_link')
        empty_text = "No nominations."

    url = django_tables2.LinkColumn(viewname='nomination_detail',
                                    kwargs={'pk': Accessor('pk')},
    )
    status = django_tables2.TemplateColumn(
        '<span class="badge-{{record.status}}">{{record.status|capfirst}}</span>',
        attrs={'cell': {'class': 'text-center'}},
    )
    claim_link = django_tables2.TemplateColumn(
        """<a href="{% url 'claim_create' nomination_pk=record.pk %}">[claim]</a>""",
        verbose_name='', orderable=False,
    )


class ClaimTable(django_tables2.Table):
    """django_tables2.Table object for lists of claims."""

    collection = django_tables2.LinkColumn()
    # tags = django_tables2.TemplateColumn(
    #     """{% load badge from cobweb_look %}
    #     <small>
    #         {% for tag in record.tags.all %}
    #             {% badge tag %}
    #         {% endfor %}
    #     </small>
    #     """, default='', orderable=False
    # )
    # claims = django_tables2.TemplateColumn(
    #     """{% load nomination_count_badge from cobweb_look %} –
    #     {% nomination_count_badge record %}
    #     <a href="{% url 'claim_create' nomination_pk=record.pk %}">[claim]</a>
    #     """,
    # )

    class Meta:
        model = Claim
        show_header = False
        fields = ('collection')
        # attrs = {'class': 'table table-hover'}
        empty_text = "No Claims."
