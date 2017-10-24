from ajax_select.fields import AutoCompleteSelectMultipleField
from ajax_select.helpers import make_ajax_form, make_ajax_field
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from django import forms
from django.forms.models import inlineformset_factory

from metadata.models import Keyword
from webresources.models import Resource

from projects.models import Project, Nomination



class ProjectForm(forms.ModelForm):

    administered_by = AutoCompleteSelectMultipleField('users')
    nominators = AutoCompleteSelectMultipleField('users', required=False)
    keywords = AutoCompleteSelectMultipleField('keywords', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(layout.Submit('submit', 'Submit'))

    class Meta:
        model = Project
        fields = [
            'name', 'administered_by', 'nomination_policy', 'nominators',
            'description', 'keywords', 'status',
        ]

class NominationForm(forms.ModelForm):

    class Meta:
        model = Nomination
        fields = ['resource', 'project', 'description', 'keywords']
        exclude = []

    keywords = AutoCompleteSelectMultipleField('keywords', required=False)

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
            