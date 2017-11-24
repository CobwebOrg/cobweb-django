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

from webresources.models import Resource

from projects.models import Project, Nomination


name_plaintext_field = Layout(
    HTML("""
        {% load cobweb_look %}
        <h3 class="click_to_edit_field col-lg-12 collapse show">
            {{object.name}}
            <a class="btn" data-toggle="collapse" href=".click_to_edit_field">
                {% icon 'edit' %}
            </a>
        </h3>
        """),
    Field('name', wrapper_class="col-lg-12 click_to_edit_field collapse"),
)
name_form_field = Field('name', wrapper_class="col-lg-12")


class ProjectForm(forms.ModelForm):
    """Project model form."""

    class Meta:
        """Metaclass for options."""

        model = Project
        fields = ('__all__')
        widgets = {
            'administered_by': autocomplete.ModelSelect2Multiple(
                url='user_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
            'nominators': autocomplete.ModelSelect2Multiple(
                url='user_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
            'nominator_blacklist': autocomplete.ModelSelect2Multiple(
                url='user_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
            'keywords': autocomplete.ModelSelect2Multiple(
                url='keyword_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
            'nomination_policy': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        """Initialize ProjectForm, adding crispy_forms helper and layout."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if self.instance.name and len(self.instance.name) > 0:
            name_field = name_plaintext_field
        else:
            name_field = name_form_field

        self.helper.layout = Layout(
            Fieldset('', name_field, css_class='row my-2'),

            Fieldset(
                '',
                Field('status', wrapper_class='col-lg-5 pb-2'),
                Field('administered_by', wrapper_class='col-lg-7 pb-2'),
                css_class='row',
            ),

            Fieldset(
                '',
                Field('description', template='metadata_field.html'),
                Field('keywords', template='metadata_field.html'),
            ),

            Fieldset(
                '',
                Field('nomination_policy', wrapper_class='col-lg-5'),
                Column(
                    UneditableField('nominators'),
                    Field('nominator_blacklist'),
                    css_class='col-lg-7'
                ),
                css_class='row',
            ),
            FormActions(
                Button('cancel', 'Cancel'),
                Submit('submit', 'Submit'),
                css_class='float-right'
            ),
        )


class NominationForm(forms.ModelForm):

    resource = forms.URLField(widget=forms.URLInput, initial='http://')

    class Meta:
        model = Nomination
        fields = ['resource', 'project', 'description', 'keywords']
        exclude = []
        fields = ('__all__')
        widgets = {
            'keywords': autocomplete.ModelSelect2Multiple(
                url='keyword_autocomplete'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('resource', template='metadata_field.html'),
            Field('project', template='metadata_field.html'),
            Field('description', template='metadata_field.html'),
            Field('keywords', template='metadata_field.html'),
            FormActions(
                Button('cancel', 'Cancel'),
                Submit('submit', 'Submit'),
                css_class='float-right'
            ),
        )

    def clean_resource(self):
        url = self.cleaned_data.get("resource")
        if not url:
            raise forms.ValidationError("Please enter a URL.")
        else:
            return Resource.objects.get_or_create(url=url)[0]


class NominateToProjectForm(NominationForm):

    class Meta(NominationForm.Meta):
        fields = ['resource', 'project', 'description', 'keywords']


class ResourceNominateForm(NominationForm):

    class Meta(NominationForm.Meta):
        fields = ['resource', 'project', 'description', 'keywords']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
