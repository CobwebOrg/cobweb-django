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
import crispy_forms.layout as crispy
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


class Field(crispy.Field):
    def __init__(self, *args, show=True, edit=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.show = show
        self.edit = edit
        if not edit:
            self.attrs['disabled'] = True

    def render(self, *args, **kwargs):
        if not self.show:
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
        # try:
        #     kwargs['css_class'] += ' pane'
        # except KeyError:
        #     kwargs['css_class'] = 'pane'
        super().__init__(Div(*args, css_class='pane d-flex flex-column'), **kwargs)


class Column(Div):
    """
    Layout object. It wraps fields in a div whose default class is "col".

    For Cobweb, we override the default django_crispy_forms Column, which uses
    the bootstrap-incompatible class name "formColumn".
    
    Example::

        Column('form_field_1', 'form_field_2')
    """
    css_class = 'col'


FormButtons = FormActions(
    Reset('reset', 'Cancel'),
    Submit('submit', 'Submit'),
    css_class='mt-auto d-flex flex-row justify-content-end',
    # field_class='d-flex flex-row justify-content-end',
)

class FormSection(Div):
    def __init__(self, *args, **kwargs):
        try:
            kwargs['css_class'] += ' form-section'
        except KeyError:
            kwargs['css_class'] = 'form-section'
        super().__init__(*args, **kwargs)


class HField(Field):
    template = 'field_horizontal.html'


class BaseHeader(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(HTML(f'<h{self.n}>'), *args, HTML(f'</h{self.n}>'), **kwargs)


class H1(BaseHeader):
    n=1


class H2(BaseHeader):
    n=2


class H3(BaseHeader):
    n=3


class H4(BaseHeader):
    n=4


class H5(BaseHeader):
    n=5


class H6(BaseHeader):
    n=6
