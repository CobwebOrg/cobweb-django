from collections import defaultdict
from inspect import isclass
from urllib.parse import urlsplit

from django import template
from django.contrib import auth
from django.db.models import Model
from django.urls import reverse
from django.utils.html import format_html, mark_safe  # , conditional_escape
from django.utils.safestring import mark_safe
from haystack.models import SearchResult

import help_text
from api.serializers import ResourceSerializer
from core.models import User, Resource, Organization
from projects.models import Project, Nomination, Claim


register = template.Library()


@register.inclusion_tag('add_nomination_link.html')
def add_nomination_link(item, user):
    if item.is_nominator(user):
        return {'link_url': item.get_add_nomination_url()}
    else:
        return {}


@register.filter
def as_link(item: Model) -> dict:
    url = item.get_absolute_url()
    if bool(urlsplit(url).netloc):
        # True for absolute URLs
        link_icon = ' ' + icon('external-link')
    else:
        link_icon = ''

    return mark_safe(f'<a href="{url}">{item}{link_icon}</a>')


@register.inclusion_tag('count_badge.html')
def count_badge(queryset):
    return {'count': queryset.count(),
            'models': (queryset.model,)}


@register.simple_tag
def claim_button(nomination, user):
    if hasattr(user, 'collections_administered') and user.collections_administered.count() > 0:
        return format_html(
            '<a href="{}" class="btn btn-primary float-right">Claim</a>',
            reverse('claim_create', kwargs={'nomination_pk': nomination.pk}),
        )
    else:
        return ''


@register.inclusion_tag('edit_link.html')
def edit_link(item, user):
    if item.is_admin(user):
        return {'edit_url': item.get_edit_url()}
    else:
        return dict()


@register.filter
@register.simple_tag
def icon(item):
    if not isinstance(item, str):
        item = item._meta.verbose_name.capitalize()

    format_args = {
        'User': ('User', 'fa-user'),
        'Tag': ('Tag', 'fa-tag'),
        'Organization': ('Organization', 'fa-university'),
        'Project': ('Project', 'fa-folder-open'),
        'Nomination': ('Nomination', 'fa-paperclip'),
        'Claim': ('Claim', 'fa-check'),
        'Holding': ('Holding', 'fa-inbox'),
        'Resource': ('Resource', 'fa-desktop'),

        'external-link': ('external link', 'fa-external-link-alt'),
        'profile': ('profile', 'fa-id-card'),

        'close': ('close', 'fa-remove'),
        'edit':  ('edit', 'fa-edit'),
        'sign_up': ('sign_up', 'fa-user-plus'),
        'reply': ('reply', 'fa-reply'),
        'search': ('search', 'fa-search'),
    }.get(item, (item.replace('-', ' '), f'fa-{item}'))

    return mark_safe(
        format_html('<span title="{}" class="fas {}"></span>', *format_args)
    )


@register.inclusion_tag('help_text/more_info.html')
def more_info(help_topic: str):
    return {'help_text': getattr(help_text, help_topic)}


@register.inclusion_tag('summary.html')
def summary(item):
    if isinstance(item.object, Project):
        summary_metadata = {
            'description': [item.description] if item.description else [],
            'tags': item.tags or [],
            'nominations': [
                format_html('<span class="badge badge-{kind}">{n}</span> {kind_cap}',
                            n=getattr(item, f'{kind}_nominations'),
                            kind=kind, kind_cap=kind[0].upper() + kind[1:])
                for kind in ('unclaimed', 'claimed', 'held')
                if getattr(item, f'{kind}_nominations') > 0
            ],
        }
    elif isinstance(item.object, Resource):
        summary_metadata = {
            'title': [item.title] if item.title else [],
            'description': [item.description] if item.description else [],
            'tags': item.tags or [],
            'subject': item.subject or [],
        }
    elif isinstance(item.object, Organization):
        summary_metadata = {
            'short_name': [item.short_name] if item.short_name else [],
            'description': [item.description] if item.description else [],
            'claims': [
                format_html('<span class="badge badge-{kind}">{n}</span> {kind}',
                            kind=kind, n=getattr(item, f'{kind}_nominations'))
                for kind in ('claimed', 'held')
                if getattr(item, f'n_{kind}') > 0
            ],
        }
    else:
        summary_metadata
        for field in ('description', 'tags'):
            try:
                summary_metadata[field] = getattr(item, field)
                if isinstance(summary_metadata[field], str) or not hasattr(item, __iter__):
                    summary_metadata[field] = [summary_metadata[field]]
            except AttributeError:
                pass

    return {'obj': item, 'summary_metadata': summary_metadata}


@register.inclusion_tag('badge.html')
def badge(item):
    return {
        'icon_name': item.__class__.__name__,
        'item': item
     }


@register.inclusion_tag('project_count_badge.html')
def project_count_badge(item):
    assert isinstance(item, Project)
    nresources = item.nominations.count()
    n_unclaimed = item.nominations.filter(claims=None).count()
    return {'claimed': nresources-n_unclaimed, 'unclaimed': n_unclaimed}


@register.inclusion_tag('nomination_count_badge.html')
def nomination_count_badge(item):
    assert isinstance(item, Nomination)
    nclaims = item.claims.count()
    return {'nclaims': nclaims}


@register.inclusion_tag('searchbar.html')
def searchbar(view_name):
    return {'view_name': view_name}


@register.filter
def model(item):
    model = None
    if isclass(item) and issubclass(item, Model):
        model = item
    elif isinstance(item, Model):
        model = type(item)
    elif isinstance(item, SearchResult):
        model = item.model
    else:
        raise ValueError(f"Filter cobweb_look.model can't handle type: {type(item)}")
    return model


@register.filter
def model_name(item):
    return item._meta.verbose_name


@register.filter
def model_name_plural(item):
    return item._meta.verbose_name_plural
    