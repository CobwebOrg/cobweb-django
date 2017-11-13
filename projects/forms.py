from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
from django.template import Template

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

from metadata.models import Keyword
from webresources.models import Resource

from projects.models import Project, Nomination


editable_title = Layout(
    HTML("""
        {% load cobweb_look %}
        <h3 class="editable_title col-lg-12 collapse show">
            {{object.name}} 
            <a class="btn" data-toggle="collapse" href=".editable_title">
                {% icon 'edit' %}
            </a>
        </h3>
        """),
    Field('name', wrapper_class="col-lg-12 editable_title collapse"),
)

class ProjectForm(forms.ModelForm):

    class Meta:
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
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset('', editable_title, css_class='row my-2'),

            Fieldset('',
                Field('status', wrapper_class='col-lg-5 pb-2'),
                Field('administered_by', wrapper_class='col-lg-7 pb-2'),
                css_class='row',
            ),

            Fieldset('',
                Field('description', template='metadata_field.html'), 
                Field('keywords', template='metadata_field.html'),
            ),

            Fieldset('',
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

    class Meta:
        model = Nomination
        fields = ['resource', 'project', 'description', 'keywords', 'metadata']
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
        self.helper.add_input(layout.Submit('submit', 'Submit'))

    def clean_resource(self):
        url = self.cleaned_data.get("resource")
        if not url:
            raise forms.ValidationError("Please enter a URL.")
        else:
            return Resource.objects.get_or_create(url = url)[0]

class NominateToProjectForm(NominationForm):

    class Meta(NominationForm.Meta):
        exclude = ['project']
        
    resource = forms.URLField(widget=forms.URLInput, initial='http://')

class ResourceNominateForm(NominationForm):

    class Meta(NominationForm.Meta):
        exclude = ['resource']
            