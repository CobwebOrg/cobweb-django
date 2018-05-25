from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms
from django.contrib.auth.models import AnonymousUser

from core.layout import (
    Pane,
    CancelButton,
    Column,
    Field,
    HField,
    HTML,
    FormActions,
    FormSection,
    Hidden,
    Layout,
    Reset,
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
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
            'nomination_policy': forms.RadioSelect,
        }

    def __init__(self, *args, admin_version=False,  **kwargs):
        """Initialize ProjectForm, adding crispy_forms helper and layout."""

        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if self.instance.title and len(self.instance.title) > 0:
            title_field = title_plaintext_field
        else:
            title_field = title_form_field

        self.helper.layout = Layout(
            Row(Column(Field('title')), css_class='d-none'),

            Row(Column(HField('description', edit=admin_version))),

            Row(
                Column(Field('status', edit=admin_version), css_class='col-md-5'),
                Column(Field('administrators', edit=admin_version), css_class='col-md-7'),
            ),

            Row(
                Field('nomination_policy', edit=admin_version, wrapper_class='col-md-5'),
                Column(
                    Field('nominators', edit=admin_version),
                    Field('nominator_blacklist', edit=admin_version, show=admin_version),
                    css_class='col-md-7'
                ),
            ),

            Row(Column(Field('tags', edit=admin_version))),

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

    def __init__(self, *args, user=AnonymousUser(), **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Column(Field('project')), css_class='d-none'),
            # Row(Column(Field('title')), css_class='d-none'),
            Row(Column(Field('resource', css_class='d-none  form-control-plaintext'))),

            Row(Column(Field('rationale'))),
            Row(Column(Field('suggested_crawl_frequency'), css_class='col-6'),
                Column(Field('suggested_crawl_end_date'), css_class='col-6')),

            Row(
                Column(
                    Reset('reset', 'Cancel'),
                    Submit('submit', 'Submit', css_class='ml-3'),
                    css_class='col-12 d-flex flex-row justify-content-end'
                )
            )
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
        template_name = 'projects/claim_form.html'
        fields = ('nomination', 'organization', 'active', 'has_holding')
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag_autocomplete'
            ),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Column(HTML('<h4>Claim</h4>'))),
            Row(Column(Field('nomination', css_class='d-none'))),
            Row(Column(Field('organization'))),
            Row(Column(Field('active'), css_class='col-6'),
                Column(Field('has_holding'), css_class='col-6')),
        )
