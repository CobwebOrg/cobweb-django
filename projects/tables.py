import django_tables2

from projects.models import Project, Nomination


class ProjectTable(django_tables2.Table):
    """django_tables2.Table object for lists of projects."""

    title = django_tables2.LinkColumn()
    nholdings = django_tables2.TemplateColumn(
        '{% load project_count_badge from cobweb_look %}'
        '{% project_count_badge record %}',
        default='', orderable=False,
    )

    class Meta:
        model = Project
        show_header = False
        fields = ['title', 'nholdings']
        # attrs = {'class': 'table table-hover'}
        empty_text = "No projects."


class NominationTable(django_tables2.Table):
    """django_tables2.Table object for lists of nominations."""

    resource = django_tables2.LinkColumn()
    keywords = django_tables2.TemplateColumn(
        """{% load badge from cobweb_look %}
        <small>
            {% for keyword in record.keywords.all %}
                {% badge keyword %}
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