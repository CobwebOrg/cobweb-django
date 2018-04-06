from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms

from core.layout import (
    CancelButton,
    Column,
    Field,
    FormActions,
    FormSection,
    Hidden,
    Layout,
    Row,
    Submit,
    title_form_field,
    title_plaintext_field,
    UneditableField,
)
from projects.models import Project, Nomination, Claim
from webresources.models import Resource
from webresources.widgets import ResourceInput


class ProjectForm(forms.ModelForm):
    """Project model form."""

    class Meta:
        """Metaclass for options."""

        model = Project
        fields = ('__all__')
        widgets = {
            'title': forms.TextInput,
            'administrators': autocomplete.ModelSelect2Multiple(
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
            'nomination_policy': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        """Initialize ProjectForm, adding crispy_forms helper and layout."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if self.instance.title and len(self.instance.title) > 0:
            title_field = title_plaintext_field
        else:
            title_field = title_form_field

        self.helper.layout = Layout(
            Row(title_field, css_class='my-2'),

            Row(
                Column(FormSection(Field('status')), css_class='col-md-5'),
                Column(FormSection(Field('administrators')), css_class='col-md-7'),
            ),

            FormSection(
                Field('description', template='metadata_field.html'),
                Field('keywords', template='metadata_field.html'),
            ),

            FormSection(
                Row(
                    Field('nomination_policy', wrapper_class='col-md-5'),
                    Column(
                        UneditableField('nominators'),
                        Field('nominator_blacklist'),
                        css_class='col-md-7'
                    ),
                )
            ),
            FormActions(
                CancelButton,
                Submit('submit', 'Submit'),
                css_class='float-right'
            ),
        )


class NominationForm(forms.ModelForm):

    resource = forms.URLField(widget=ResourceInput, initial='http://')

    class Meta:
        model = Nomination
        exclude = []
        widgets = {
            'title': forms.TextInput,
            'keywords': autocomplete.ModelSelect2Multiple(
                url='keyword_autocomplete'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                Field('title', template='metadata_field.html'),
                Field('resource', template='metadata_field.html'),
            Row(
                Column(FormSection(Field('project')), css_class='col-md-7'),
                Column(FormSection(Field('status')), css_class='col-md-5'),
            ),
            FormSection(
                Field('description', template='metadata_field.html'),
                Field('keywords', template='metadata_field.html'),
            ),
            FormActions(
                CancelButton,
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


class ClaimForm(forms.ModelForm):

    class Meta:
        model = Claim
        fields = ('__all__')
        widgets = {
            'keywords': autocomplete.ModelSelect2Multiple(
                url='keyword_autocomplete'
            ),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.layout = Layout(
        #     Field('nomination', css_class='form-control-plaintext'),
        #     Field('collection'),
        #     Field('description'),
        #     Field('keywords'),
        #     FormActions(
        #         CancelButton,
        #         Submit('submit', 'Submit'),
        #         css_class='float-right'
        #     ),
        # )
