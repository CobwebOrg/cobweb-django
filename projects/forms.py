from crispy_forms.helper import FormHelper
from crispy_forms import layout
from django.forms import  ModelForm, URLField, URLInput, ValidationError

from projects.models import Project, Nomination
from webresources.models import Resource


class ProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(layout.Submit('submit', 'Submit'))

    class Meta:
        model = Project
        fields = ['name', 'description']

class NominationForm(ModelForm):

    class Meta:
        model = Nomination
        fields = ['resource', 'description']

    resource = URLField(widget=URLInput, initial='http://') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(layout.Submit('submit', 'Submit'))

    def clean_resource(self):
        location = self.cleaned_data.get("resource")
        if not location:
            raise ValidationError("Please enter a URL.")
        else:
            return Resource.objects.get_or_create(location = location)[0]