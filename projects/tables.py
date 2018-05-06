import django_tables2
from django_tables2.utils import Accessor

from projects.models import Project, Nomination, Claim


class ProjectTable(django_tables2.Table):
    """django_tables2.Table object for lists of projects."""

    title = django_tables2.LinkColumn(viewname='project_detail', kwargs={'pk': Accessor('pk')})#,
                                    #   text=lambda record: print(record, record.title, record.get_stored_fields()['title']))
    unclaimed_nominations = django_tables2.Column()
    claimed_nominations = django_tables2.Column()

    class Meta:
        model = Project
        fields = ['title', 'unclaimed_nominations', 'claimed_nominations']
        attrs = {'class': 'table table-hover'}
        empty_text = "No projects."
        order_by = ('-impact_factor', '-pk')


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
