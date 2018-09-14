from copy import deepcopy

from django import template
from django.utils.html import format_html

from jargon.terms import TERMS


register = template.Library()


@register.inclusion_tag('jargon/term.html')
def term(term_key: str, *string_methods: str, inflection=None) -> dict:
    term_info = deepcopy(TERMS[term_key])

    term_info['key'] = term_key

    if inflection:
        term_info['term'] = term_info[f'term-{inflection}']
    for method_name in string_methods:
        if method_name == 'capitalize':
            # override built-in str.capitalize(), which lowercases all but 1st letter
            term_info['term'] = term_info['term'][0].upper() + term_info['term'][1:]
        else:
            term_info['term'] = getattr(term_info['term'], method_name)()

    return term_info

@register.inclusion_tag('jargon/term.html')
def term_plural(term_key: str, *string_methods: str) -> dict:
    return term(term_key, *string_methods, inflection='plural')