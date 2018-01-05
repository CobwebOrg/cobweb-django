from collections import defaultdict
from django import template
from django.db.models import Model
from django.utils.html import format_html  # , conditional_escape
# from django.utils.safestring import mark_safe

from archives.models import Collection
from projects.models import Project


register = template.Library()

ICONS = defaultdict(str, {
    'User': 'fa-user',
    'Keyword': 'fa-tag',
    'Organization': 'fa-institution',
    'Project': 'fa-tasks',
    'Collection': 'fa-archive',
    'Nomination': 'fa-sign-out',
    'Claim': 'fa-sign-in',
    'Holding': 'fa-inbox',
    'Resource': 'fa-link',

    'profile': 'fa-id-card',

    'close': 'fa-remove',
    'edit':  'fa-edit',
    'sign_up': 'user-plus',
    'reply': 'fa-reply',
    'search': 'fa-search',
})


@register.inclusion_tag('add_nomination_link.html')
def add_nomination_link(item, user):
    if item.is_nominator(user):
        return {'link_url': item.get_add_nomination_url()}
    else:
        return {}


@register.filter
def as_link(item):
    return format_html(
        '<a href="{url}">{item}</a>',
        item=item,
        url=item.get_absolute_url()
    )


@register.inclusion_tag('edit_link.html')
def edit_link(item, user):
    if item.is_admin(user):
        return {'edit_url': item.get_edit_url()}
    else:
        return dict()


@register.inclusion_tag('icon.html')
def icon(icon_name):
    print('>>>' + icon_name, type(icon_name), isinstance(icon_name, Model))
    if isinstance(icon_name, Model):
        icon_name = icon_name._meta.verbose_name
    assert isinstance(icon_name, str)
    return {'title': icon_name, 'icon': ICONS[icon_name]}


@register.inclusion_tag('core/metadata_card.html')
def metadata_card(item, **kwargs):
    kwargs['item'] = item
    return kwargs


@register.inclusion_tag('pill.html')
def pill(item):
    return {
        'icon_name': item.__class__.__name__,
        'item': item
     }


@register.inclusion_tag('resource_count_badge.html')
def resource_count_badge(item):
    assert type(item) is Project or type(item) is Collection
    if type(item) is Project:
        nresources = item.nominations.count()
    elif type(item) is Collection:
        nresources = item.holdings.count()
    return {'nresources': nresources}


@register.inclusion_tag('count_badge.html')
def count_badge(queryset):
    return {'count': queryset.count(),
            'models': (str(queryset.model),)}


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
