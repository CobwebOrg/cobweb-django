from crispy_forms.helper import FormHelper
from crispy_forms import layout
from dal import autocomplete
from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory

from metadata.models import Keyword
from webresources.models import Resource

from projects.models import Project, Nomination



class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('__all__')
        widgets = {
            'administered_by': autocomplete.ModelSelect2Multiple(
                url='user_autocomplete'
            ),
            'nominators': autocomplete.ModelSelect2Multiple(
                url='user_autocomplete'
            ),
            'keywords': autocomplete.ModelSelect2Multiple(
                url='keyword_autocomplete'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = layout.Layout(
            layout.Field('name'),
            layout.Fieldset('Project Settings',
                layout.Div(
                    layout.Field('administered_by'), 
                    layout.Field('status'),
                    css_class='col-lg-6',
                ),
                layout.Div(
                    layout.Field('nomination_policy'), 
                    layout.Field('nominators'), 
                    css_class='col-lg-6',
                ),
                css_class='row',
            ),
            layout.Fieldset('Project Metadata',
                layout.Div(layout.Field('description'), css_class='col-lg-6'), 
                layout.Div(layout.Field('keywords'), css_class='col-lg'),
                css_class='row',
            ),
            layout.ButtonHolder(
                layout.Submit('submit', 'Submit'),
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
            