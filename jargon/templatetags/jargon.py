from django import template

from jargon.terms import TERMS


register = template.Library()


@register.inclusion_tag('jargon/term.html')
def term(term_key: str, *string_methods: str, inflection=None) -> dict:
    term_info = TERMS[term_key]
    if inflection:
        term_info['term'] = term_info[f'term-{inflection}']
    for method_name in string_methods:
        term_info['term'] = getattr(term_info['term'], method_name)()
    return term_info

@register.inclusion_tag('jargon/term.html')
def term_plural(term_key: str, *string_methods: str) -> dict:
    term_info = TERMS[term_key]
    term_info['term'] = term_info['term-plural']
    for method_name in string_methods:
        term_info['term'] = getattr(term_info['term'], method_name)()
    return term_info