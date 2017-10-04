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


class MDBaseInlineFormset(forms.BaseInlineFormset):
    # Use as a base class for specialized inline formsets, e.g.:
    # class ModelMDInlineFormset(metadata.forms.MetadatumBaseInline): 
    #     model = Model.metadata.through

    extra = 0
    show_change_link = True

    def md_name(self, instance):
        if instance.id:
            return(str(instance.metadatum))
    md_name.short_description = 'Metadata'
    fields = [ 'md_name' ]
    readonly_fields = fields