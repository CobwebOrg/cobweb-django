from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms

from core.layout import (
    Pane,
    CancelButton,
    Column,
    Field,
    HField,
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
from core.models import Resource
from core.widgets import ResourceInput


class ProjectForm(forms.ModelForm):
    """Project model form."""

    class Meta:
        """Metaclass for options."""

        model = Project
        fields = ('__all__')
        widgets = {
            'title': forms.TextInput,
            # 'administrators': autocomplete.ModelSelect2Multiple(
            #     url='user_autocomplete',
            #     attrs={'data-allow-clear': 'false'},
            # ),
            # 'nominators': autocomplete.ModelSelect2Multiple(
            #     url='user_autocomplete',
            #     attrs={'data-allow-clear': 'false'},
            # ),
            # 'nominator_blacklist': autocomplete.ModelSelect2Multiple(
            #     url='user_autocomplete',
            #     attrs={'data-allow-clear': 'false'},
            # ),
            # 'tags': autocomplete.ModelSelect2Multiple(
            #     url='tag_autocomplete',
            #     attrs={'data-allow-clear': 'false'},
            # ),
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
            Pane(
                Row(Column(Field('title')), css_class='d-none'),
                
                Row(Column(HField('description'))),

                Row(
                    Column(Field('status'), css_class='col-md-5'),
                    Column(Field('administrators'), css_class='col-md-7'),
                ),

                Row(
                    Field('nomination_policy', wrapper_class='col-md-5'),
                    Column(
                        UneditableField('nominators'),
                        Field('nominator_blacklist'),
                        css_class='col-md-7'
                    ),
                ),

                Row(Column(Field('tags'))),

                Row(
                    Column(
                        FormActions(
                            CancelButton,
                            Submit('submit', 'Submit'),
                            css_class='justify-content-end'
                        ),
                        css_class='col-12'
                    )
                )
            )
        )


class NominationForm(forms.ModelForm):

    resource = forms.URLField(widget=ResourceInput, initial='http://')

    class Meta:
        model = Nomination
        fields = ('__all__')
        widgets = {
            'title': forms.TextInput,
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag_autocomplete'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                Field('title', template='field_horizontal.html'),
                Field('resource', template='field_horizontal.html'),
            Row(
                Column(FormSection(Field('project')), css_class='col-md-7'),
                Column(FormSection(Field('status')), css_class='col-md-5'),
            ),
            FormSection(
                Field('description', template='field_horizontal.html'),
                Field('tags', template='field_horizontal.html'),
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
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag_autocomplete'
            ),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.layout = Layout(
        #     Field('nomination', css_class='form-control-plaintext'),
        #     Field('collection'),
        #     Field('description'),
        #     Field('tags'),
        #     FormActions(
        #         CancelButton,
        #         Submit('submit', 'Submit'),
        #         css_class='float-right'
        #     ),
        # )
