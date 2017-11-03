from collections import defaultdict
from django import template
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe


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

    'profile': 'fa-id-card', #'fa-id-card-o',

    'close': ' fa-institution fa-remove',
    'edit':  'fa-pencil-square-o',
    'sign_up': 'user-plus',
    'reply': 'fa-reply',
    'search': 'fa-search',
})

@register.inclusion_tag('add_nomination_link.html')
def add_nomination_link(item, user):
    if item.is_nominator(user):
        return {'link_url': item.get_add_nomination_url()}

@register.inclusion_tag('edit_link.html')
def edit_link(item, user):
    if item.is_admin(user):
        return {'edit_url': item.get_edit_url()}
    else:
        return dict()

@register.inclusion_tag('icon.html')
def icon(icon_name):
    return {'icon': ICONS[icon_name]}

@register.inclusion_tag('core/metadata_card.html')
def metadata_card(item, title=None):
    if title is None:
        title = str(item)
    return {'item': item, 'title': title}

@register.inclusion_tag('pill.html')
def pill(item):
    return {
        'icon_name': item.__class__.__name__,
        'item': item
     }

@register.filter
def resourceset_model_name(item):
    return item.get_resource_set()._meta.verbose_name

@register.inclusion_tag('searchbar.html')
def searchbar(view_name):
    return { 'view_name': view_name }

@register.filter
def model_name(item):
    return item._meta.verbose_name