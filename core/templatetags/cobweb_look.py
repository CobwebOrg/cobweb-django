from collections import defaultdict
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()

ICONS = defaultdict(str, {
    'User': 'fa-user',
    'Keyword': 'fa-tag',
    'edit':  'fa-pencil-square-o',
    'sign_up': 'user-plus',
})

@register.inclusion_tag('add_nomination_link.html')
def add_nomination_link(item, user):
    if item.can_nominate(user):
        return {'link_url': item.get_add_nomination_url()}

@register.inclusion_tag('edit_link.html')
def edit_link(item, user):
    if item.can_administer(user):
        return {'edit_url': item.get_edit_url()}
    else:
        return dict()

@register.inclusion_tag('icon.html')
def icon(icon_name):
    return {'icon': ICONS[icon_name]}

@register.inclusion_tag('pill.html')
def pill(item):
    return {
        'color': 'info',
        'icon_name': item.__class__.__name__,
        'item': item
     }

@register.inclusion_tag('pill_link.html')
def pill_link(item):
    return pill(item) # same dict - template makes the difference