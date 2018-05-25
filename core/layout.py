from crispy_forms.layout import (
    BaseInput,
    Button,
    ButtonHolder,
    # Column,
    Div,
    Fieldset,
    HTML,
    Hidden,
    Layout,
    LayoutObject,
    MultiField,
    MultiWidgetField,
    Reset,
    Row,
    Submit,
    # TemplateNameMixin,
)
from crispy_forms.layout import Field as CrispyField
from crispy_forms.bootstrap import (
    Accordion,
    AccordionGroup,
    Alert,
    AppendedText,
    Container,
    ContainerHolder,
    FieldWithButtons,
    FormActions,
    InlineCheckboxes,
    InlineField,
    InlineRadios,
    PrependedAppendedText,
    PrependedText,
    StrictButton,
    Tab,
    TabHolder,
    UneditableField,
)


class Field(CrispyField):
    def __init__(self, *args, show=True, edit=False, **kwargs):
        self.show = show
        self.edit = edit
        if not self.edit:
            if 'css_class' in kwargs:
                kwargs['css_class'] += ' form-control-plaintext'
            else:
                kwargs['css_class'] = 'form-control-plaintext'
        super().__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        if self.show == False:
            return ''
        else:
            return super().render(*args, **kwargs)


title_plaintext_field = Layout(
    HTML("""
        {% load cobweb_look %}
        <h3 class="click_to_edit_field col-md-12 collapse show">
            {{object.title}}
            <a class="btn" data-toggle="collapse" href=".click_to_edit_field">
                {% icon 'edit' %}
            </a>
        </h3>
        """),
    Field('title', wrapper_class="col-md-12 click_to_edit_field collapse"),
)
title_form_field = Field('title', wrapper_class="col-md-12")


CancelButton = HTML("""
    <a href="{{object.get_absolute_url}}" class="btn btn-light btn btn-outline-dark mr-1">
        Cancel
    </a>
""")

    
class Pane(Div):
    def __init__(self, *args, **kwargs):
        try:
            kwargs['css_class'] += ' pane'
        except KeyError:
            kwargs['css_class'] = 'pane'
        super().__init__(*args, **kwargs)


class Column(Div):
    """
    Layout object. It wraps fields in a div whose default class is "col".

    For Cobweb, we override the default django_crispy_forms Column, which uses
    the bootstrap-incompatible class name "formColumn".
    
    Example::

        Column('form_field_1', 'form_field_2')
    """
    css_class = 'col'


class FormSection(Div):
    def __init__(self, *args, **kwargs):
        try:
            kwargs['css_class'] += ' form-section'
        except KeyError:
            kwargs['css_class'] = 'form-section'
        super().__init__(*args, **kwargs)

class HField(Field):
    template = 'field_horizontal.html'