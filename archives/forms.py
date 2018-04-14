from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms

from crispy_forms.layout import (
    BaseInput,
    Button,
    ButtonHolder,
    Column,
    Div,
    Field,
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

from core.models import Resource

from archives.models import Collection


class AutoField(Field):
    """Uneditable, plaintext field to layer javascript edit function on."""

    def __init__(self, *args, **kwargs):
        try:
            kwargs['css_class'] += ' form-control-plaintext'
        except KeyError:
            kwargs['css_class'] = 'form-control-plaintext'
        super().__init__(*args, **kwargs)

CancelButton = HTML("""
    <a href="{{object.get_absolute_url}}" class="btn btn-light btn btn-outline-dark mr-1">
        Cancel
    </a>
""")

class FormSection(Div):
    def __init__(self, *args, **kwargs):
        try:
            kwargs['css_class'] += ' form-section'
        except KeyError:
            kwargs['css_class'] = 'form-section'
        super().__init__(*args, **kwargs)


class CollectionForm(forms.ModelForm):
    """Collection model form."""

    class Meta:
        """Metaclass for options."""

        model = Collection
        fields = ('__all__')
        widgets = {
            'administrators': autocomplete.ModelSelect2Multiple(
                url='user_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
        }

    def __init__(self, *args, **kwargs):
        """Initialize CollectionForm, adding crispy_forms helper and layout."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Row(HTML("<h3>{{object.title}}</h3>"), css_class='my-2'),

            Row(
                Column(
                    FormSection(Field('identifier')),
                    css_class='col-md-5'
                ),
                Column(
                    FormSection(Field('administrators')),
                    css_class='col-md',
                ),
            ),

            Row(
                Column(FormSection(Field('metadata')), css_class='col-md-12'),
            ),

            FormActions(
                CancelButton,
                Submit('submit', 'Submit'),
                css_class='float-right'
            ),

        )
