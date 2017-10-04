from ajax_select.fields import AutoCompleteSelectMultipleField
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from django import forms

from projects.models import Project, Nomination
from webresources.models import Resource



class ProjectForm(forms.ModelForm):

    administered_by = AutoCompleteSelectMultipleField('users')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(layout.Submit('submit', 'Submit'))

    class Meta:
        model = Project
        fields = ['name', 'administered_by', 'description']


class NominationForm(forms.ModelForm):

    class Meta:
        model = Nomination
        fields = ['resource', 'description']

    resource = forms.URLField(widget=forms.URLInput, initial='http://') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(layout.Submit('submit', 'Submit'))

    def clean_resource(self):
        location = self.cleaned_data.get("resource")
        if not location:
            raise forms.ValidationError("Please enter a URL.")
        else:
            return Resource.objects.get_or_create(location = location)[0]