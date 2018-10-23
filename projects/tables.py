import django_tables2
from django.template.loader import get_template
from django.utils.html import format_html, mark_safe
from django_tables2.utils import Accessor

import help_text
from core.tables import CobwebBaseTable
from projects.models import Claim, Nomination, Project


class ProjectTable(CobwebBaseTable):
    """django_tables2.Table object for lists of projects."""

    class Meta(CobwebBaseTable.Meta):
        model = Project
        fields = ('title', 'unclaimed_nominations',
                  'claimed_nominations', 'held_nominations')
        empty_text = "No projects."

    title = django_tables2.LinkColumn(
        viewname='project',
        kwargs={'pk': Accessor('pk')},
    )
    unclaimed_nominations = django_tables2.Column(
        verbose_name=mark_safe('Unclaimed ')
            + get_template('help_text/more_info.html')
            .render(context={'help_text': help_text.N_UNCLAIMED}),
        attrs={'cell': {'class': 'text-center'}},
    )
    claimed_nominations = django_tables2.Column(
        verbose_name=mark_safe('Claimed ')
            + get_template('help_text/more_info.html')
            .render(context={'help_text': help_text.N_CLAIMED}),
        attrs={'cell': {'class': 'text-center'}},
    )
    held_nominations = django_tables2.Column(
        verbose_name=mark_safe('Held ')
            + get_template('help_text/more_info.html')
            .render(context={'help_text': help_text.N_HELD}),
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


class UserProjectsTable(ProjectTable):
    """django_tables2.Table object for lists of projects."""

    class Meta(ProjectTable.Meta):
        fields = ('title', 'n_unclaimed',
                  'n_claimed', 'n_held')
        exclude = ['unclaimed_nominations', 'claimed_nominations',
                   'held_nominations']

    n_unclaimed = django_tables2.Column(
        verbose_name=mark_safe('Unclaimed ')
            + get_template('help_text/more_info.html')
            .render(context={'help_text': help_text.N_UNCLAIMED}),
        attrs={'cell': {'class': 'text-center'}},
    )
    n_claimed = django_tables2.Column(
        verbose_name=mark_safe('Claimed ')
            + get_template('help_text/more_info.html')
            .render(context={'help_text': help_text.N_CLAIMED}),
        attrs={'cell': {'class': 'text-center'}},
    )
    n_held = django_tables2.Column(
        verbose_name=mark_safe('Held ')
            + get_template('help_text/more_info.html')
            .render(context={'help_text': help_text.N_HELD}),
        attrs={'cell': {'class': 'text-center'}},
    )

    def render_n_unclaimed(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="badge-unclaimed">{}</span>',
                               value)

    def render_n_claimed(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="badge-claimed">{}</span>',
                               value)

    def render_n_held(self, value):
        if value == 0:
            return ''
        else:
            return format_html('<span class="badge-held">{}</span>',
                               value)


class NominationColumn(django_tables2.LinkColumn):

    def text(self, record):
        return record.name
    
    def render_link(self, uri, record, value, attrs=None):
        return super().render_link(uri, record, value, attrs=None)

class NominationTable(CobwebBaseTable):
    """django_tables2.Table object for lists of nominations."""

    class Meta(CobwebBaseTable.Meta):
        model = Nomination
        fields = ('name', 'project', 'status')  #, 'claim_link')
        # exclude = ('project',)
        empty_text = "No nominations."

    name = django_tables2.LinkColumn(
        viewname='nomination_update',
        kwargs={'project_pk': Accessor('project_pk'),
                'url': Accessor('url')},
        verbose_name='Nomination',
    )

    project = django_tables2.LinkColumn(
        viewname='nomination_update',
        kwargs={'project_pk': Accessor('project_id'),
                'url': Accessor('resource.url')},
        verbose_name='In project',
    )

    status = django_tables2.TemplateColumn(
        '<span class="badge-{{record.status}}">{{record.status|capfirst}}</span>',
        attrs={'cell': {'class': 'text-center'}},
    )
    
    # claim_link = django_tables2.LinkColumn(
    #     viewname='nomination_update',
    #     kwargs={'project_pk': Accessor('project_pk'),
    #             'url': Accessor('url')},
    #     text='[claim]', verbose_name='', orderable=False,
    # )


class ClaimTable(CobwebBaseTable):
    """django_tables2.Table object for lists of claims."""

    class Meta(CobwebBaseTable.Meta):
        model = Claim
        fields = ('claim_type', 'nomination', 'organization', 'link')
        empty_text = "No Claims."

    nomination = django_tables2.LinkColumn(viewname='nomination',
                                    kwargs={'pk': Accessor('pk')})
    organization = django_tables2.LinkColumn(viewname='organization',
                                    kwargs={'slug': Accessor('organization.slug')})
    link = django_tables2.TemplateColumn(
        '<a href={{record.get_absolute_url}} class="linklet">[details]</a>',
        verbose_name='',
    )

    claim_type = django_tables2.TemplateColumn("""
        {% if record.has_holding %}
            <span class="badge-held">Held</span>
        {% else %}
            <span class="badge-claimed">Claimed</span>
        {% endif %}
    """, verbose_name="Claim type", orderable=False)
