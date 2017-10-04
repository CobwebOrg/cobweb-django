from ajax_select.fields import AutoCompleteSelectField
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from django import forms  

from metadata.models import Metadatum


class MetadatumForm(forms.ModelForm):

    md_property = AutoCompleteSelectField('md_property')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.add_input(layout.Submit('submit', 'Submit'))

    class Meta:
        model = Metadatum
        fields = [ 'md_property', 'name' ]

