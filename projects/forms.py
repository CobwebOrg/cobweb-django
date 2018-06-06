from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms
from django.contrib.auth.models import AnonymousUser
from django.utils.html import format_html

from core.layout import *
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

    def __init__(self, *args, editable=False,  **kwargs):
        """Initialize ProjectForm, adding crispy_forms helper and layout."""

        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if self.instance.title and len(self.instance.title) > 0:
            title_field = title_plaintext_field
            title_row = Row(Column(HField('title')), css_class='d-none')
        else:
            title_field = title_form_field
            title_row = Row(Column(HField('title', edit=editable)))

        self.helper.layout = Layout(
            title_row,

            Row(Column(HField('description', edit=editable))),

            Row(
                Column(Field('status', edit=editable), css_class='col-md-5'),
                Column(Field('administrators', edit=editable), css_class='col-md-7'),
            ),

            Row(
                Field('nomination_policy', edit=editable, wrapper_class='col-md-5'),
                Column(
                    Field('nominators', edit=editable),
                    Field('nominator_blacklist', edit=editable, show=editable),
                    css_class='col-md-7'
                ),
            ),

            Row(Column(Field('tags', edit=editable))),
        )

        if editable:
            self.helper.layout.append(
                Row(
                    Column(
                        FormActions(
                            CancelButton,
                            Submit('submit', 'Submit'),
                            css_class='w-100 flex-row justify-content-end'
                        ),
                    )
                )
            )


class NominationForm(forms.ModelForm):
    class Meta:
        model = Nomination
        fields = ('__all__')
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
        }
    
    resource = forms.URLField(widget=ResourceInput, initial='http://')

    def __init__(self, *args, editable=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        proj_header = HTML(format_html('<small><a href="{}"> Project: {}</a></small>',
                                       self.initial['project'].get_absolute_url(),
                                       str(self.initial['project'])))
        if hasattr(self.instance, 'pk') and self.instance.pk is not None:
            nom_header = HTML(format_html('<a href="{}">NOMINATION:</a> {}',
                                          instance.get_absolute_url(),
                                          instance.name))
        else:
            nom_header = HTML('NEW NOMINATION')
        
        self.helper.layout = Layout(
            Div(
                Div(H2(proj_header)),
                Div(H3(nom_header)),
                css_class='px-3 pt-0 pb-2 w-100'
            ),

            Row(
                Pane(
                    Row(Column(HTML('<h4>About the Resource</h4>'))),
                    
                    Row(Column(HField('resource', edit=editable))),
                    Row(Column(HField('title', edit=editable))),
                    Row(Column(HField('description', edit=editable))),
                    Row(Column(Field('tags', edit=editable))),
                    Row(Column(Field('language', edit=editable))),
                    css_class='col-7'
                ),

                Pane(
                    Row(Column(HTML('<h4>Nomination Info</h4>'))),

                    Field('project', type='hidden', edit=editable),
                    Field('nominated_by', type='hidden', edit=editable),
                    Row(Column(Field('rationale', edit=editable))),
                    Row(Column(Field('suggested_crawl_frequency', edit=editable), css_class='col-6'),
                        Column(Field('suggested_crawl_end_date', edit=editable), css_class='col-6')),
                    FormButtons,
                    css_class='col-5'
                ),
                css_class='flex-grow-1'
            )
        )
        self.helper.form_class='h-100 d-flex flex-column pb-2'

    def clean_resource(self):
        url = self.cleaned_data.get("resource")
        if not url:
            raise forms.ValidationError("Please enter a URL.")
        else:
            return Resource.objects.get_or_create(url=url)[0]


class NominationDisplayForm(forms.ModelForm):
    class Meta:
        model = Nomination
        fields = ('__all__')
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
        }

    def __init__(self, *args, editable=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Column(HField('title'))),
            Row(Column(HField('description'))),
            Row(Column(Field('tags'))),
            Row(Column(Field('language'))),

            Row(Column(HTML('<h4>Nomination Info</h4>'))),

            Field('project', type='hidden'),
            Field('nominated_by', type='hidden'),
            Row(Column(Field('rationale'))),
            Row(Column(Field('suggested_crawl_frequency'), css_class='col-6'),
                Column(Field('suggested_crawl_end_date'), css_class='col-6')),
        )


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        template_name = 'projects/claim_form.html'
        fields = ('nomination', 'organization', 'active', 'has_holding')
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag_autocomplete',
                attrs={'data-allow-clear': 'false'},
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
