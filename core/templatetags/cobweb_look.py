from collections import defaultdict
from django import template
from django.contrib import auth
from django.db.models import Model
from django.urls import reverse
from django.utils.html import format_html  # , conditional_escape
from django.utils.safestring import mark_safe

from archives.models import Collection, Holding
from core.models import User
from projects.models import Project, Nomination, Claim
from webresources.models import Resource


register = template.Library()


@register.inclusion_tag('add_nomination_link.html')
def add_nomination_link(item, user):
    if item.is_nominator(user):
        return {'link_url': item.get_add_nomination_url()}
    else:
        return {}


@register.filter
def as_link(item):
    assert isinstance(item, Model), f"{repr(item)} is {type(item)}, not {Model}"
    return format_html(
        '<a href="{url}">{item_name}</a>',
        item_name=item,
        url=item.get_absolute_url()
    )


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


@register.simple_tag
def cobweb_site_section(item):
    try:
        section = {
            Project: 'Project',
            Nomination: 'Project',
            Claim: 'Project',
            Collection: 'Collection',
            Holding: 'Collection',
            Resource: 'Resource'
        }[item]
    except KeyError:
        try:
            section = model_name(item).title_case()
        except AttributeError:
            section = item
    print(f'###{section}###')

    return section


@register.inclusion_tag('edit_link.html')
def edit_link(item, user):
    if item.is_admin(user):
        return {'edit_url': item.get_edit_url()}
    else:
        return dict()


@register.simple_tag
def icon(item):
    if not isinstance(item, str):
        item = item._meta.verbose_name.capitalize()

    format_args = {
        'User': ('User', 'fa-user'),
        'Keyword': ('Keyword', 'fa-tag'),
        'Organization': ('Organization', 'fa-institution'),
        'Project': ('Project', 'fa-tasks'),
        'Collection': ('Collection', 'fa-archive'),
        'Nomination': ('Nomination', 'fa-paperclip'),
        'Claim': ('Claim', 'fa-check'),
        'Holding': ('Holding', 'fa-inbox'),
        'Resource': ('Resource', 'fa-link'),

        'profile': ('profile', 'fa-id-card'),

        'close': ('close', 'fa-remove'),
        'edit':  ('edit', 'fa-edit'),
        'sign_up': ('sign_up', 'fa-user-plus'),
        'reply': ('reply', 'fa-reply'),
        'search': ('search', 'fa-search'),
    }[item]

    return mark_safe(
        format_html('<span title="{}" class="fas {}"></span>', *format_args)
    )

@register.inclusion_tag('core/metadata_card.html')
def metadata_card(item, **kwargs):
    kwargs['item'] = item
    return kwargs


@register.inclusion_tag('badge.html')
def badge(item):
    return {
        'icon_name': item.__class__.__name__,
        'item': item
     }


@register.inclusion_tag('resource_count_badge.html')
def resource_count_badge(item):
    assert type(item) is Resource
    nominations = item.nominations.count()
    n_unclaimed = item.nominations.filter(claims=None).count()
    holdings = item.holdings.count()
    return {
        'claimed': nominations-n_unclaimed,
        'unclaimed': n_unclaimed,
        'holdings': holdings,
    }


@register.inclusion_tag('project_count_badge.html')
def project_count_badge(item):
    assert type(item) is Project
    nresources = item.nominations.count()
    n_unclaimed = item.nominations.filter(claims=None).count()
    return {'claimed': nresources-n_unclaimed, 'unclaimed': n_unclaimed}


@register.inclusion_tag('collection_count_badge.html')
def collection_count_badge(item):
    assert type(item) is Collection
    nresources = item.holdings.count()
    return {'holdings': nresources}


@register.inclusion_tag('nomination_count_badge.html')
def nomination_count_badge(item):
    assert type(item) is Nomination
    nclaims = item.claims.count()
    return {'nclaims': nclaims}


@register.filter
def resourceset_model_name(item):
    return item.get_resource_set()._meta.verbose_name


@register.inclusion_tag('searchbar.html')
def searchbar(view_name):
    return {'view_name': view_name}


@register.filter
def model_name(item):
    return item._meta.verbose_name


@register.filter
def model_name_plural(item):
    return item._meta.verbose_name_plural
