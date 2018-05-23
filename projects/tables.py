from django.utils.html import format_html
import django_tables2
from django_tables2.utils import Accessor

from core.tables import CobwebBaseTable
from projects.models import Project, Nomination, Claim


class ProjectTable(CobwebBaseTable):
    """django_tables2.Table object for lists of projects."""

    title = django_tables2.LinkColumn(
        viewname='project_detail',
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

    class Meta(CobwebBaseTable.Meta):
        model = Project
        fields = ('title', 'unclaimed_nominations',
                  'claimed_nominations', 'held_nominations')
        empty_text = "No projects."

    def render_unclaimed_nominations(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="unclaimed-count">{}</span>',
                               value)

    def render_claimed_nominations(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="claimed-count">{}</span>',
                               value)

    def render_held_nominations(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="held-count">{}</span>',
                               value)
    

class NominationTable(django_tables2.Table):
    """django_tables2.Table object for lists of nominations."""

    name = django_tables2.LinkColumn()
    tags = django_tables2.TemplateColumn(
        """{% load badge from cobweb_look %}
        <small>
            {% for tag in record.tags.all %}
                {% badge tag %}
            {% endfor %}
        </small>
        """, default='', orderable=False
    )
    claims = django_tables2.TemplateColumn(
        """{% load nomination_count_badge from cobweb_look %} –
        {% nomination_count_badge record %}
        <a href="{% url 'claim_create' nomination_pk=record.pk %}">[claim]</a>
        """,
    )

    class Meta:
        model = Nomination
        show_header = False
        fields = []
        # attrs = {'class': 'table table-hover'}
        empty_text = "No nominations."


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
        fields = []
        # attrs = {'class': 'table table-hover'}
        empty_text = "No Claims."
