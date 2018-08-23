from crispy_forms.helper import FormHelper
from dal import autocomplete
from django import forms
from django.contrib.auth.models import AnonymousUser
from django.forms import DateField, DateInput
from django.urls import reverse
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
                attrs={'data-allow-clear': 'false',
                       'data-width': '100%'},
            ),
            'nominators': autocomplete.ModelSelect2Multiple(
                url='user_autocomplete',
                attrs={'data-allow-clear': 'false',
                       'data-width': '100%'},
            ),
            'nominator_blacklist': autocomplete.ModelSelect2Multiple(
                url='user_autocomplete',
                attrs={'data-allow-clear': 'false',
                       'data-width': '100%'},
            ),
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag_autocomplete',
                attrs={'data-allow-clear': 'false',
                       'data-width': '100%'},
            ),
        }

    def __init__(self, *args, editable=False,  **kwargs):
        """Initialize ProjectForm, adding crispy_forms helper and layout."""

        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if hasattr(self.instance, 'pk') and self.instance.pk is not None:
            form_buttons_kwargs = {
                'confirm_title': 'Save changes',
                'confirm_text': 'Click the submit button to save changes to this project or click on cancel to return to Cobweb without adding the new project.',
            }
        else:
            form_buttons_kwargs = {
                'confirm_title': 'Add new project',
                'confirm_text': 'Click the submit button to add this project to Cobweb or click on cancel to return to Cobweb without adding the new project.',
            }

        self.helper.layout = Layout(
            HField('title', edit=editable),

            FormSection(
                Row(Column(HField('description', edit=editable))),

                Row(
                    Field('status', edit=editable, wrapper_class='col-md-5'),
                    Field('administrators', edit=editable, wrapper_class='col-md-7'),
                ),
            ),

            FormSection(
                Row(
                    Field(Column('nomination_policy', edit=editable), css_class='col-md-5'),
                    Column(
                        Field('nominators', edit=editable),
                        Field('nominator_blacklist', edit=editable, show=editable),
                        css_class='col-md-7'
                    ),
                ),
            ),

            FormSection(Row(Column(Field('tags', edit=editable)))),

            form_buttons(**form_buttons_kwargs) if editable else HTML(''),
        )

def resource_info(editable=False):
    return Layout(
        Row(Column(HField('resource', edit=editable))),
        Row(Column(HField('title', edit=editable))),
        Row(Column(HField('description', edit=editable))),
        Row(Column(Field('tags', edit=editable))),
        Row(Column(Field('language', edit=editable))),
    )

def nomination_info(editable=False, form_buttons_kwargs={}):
    return Layout(
        FormSection(
            Field('project', type='hidden'),
            Field('nominated_by', type='hidden'),
            Row(Column(Field('rationale', edit=editable))),
        ),
        FormSection(crawl_scope_fields(editable=editable)),
        form_buttons(**form_buttons_kwargs) if editable else HTML(''),
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
            'crawl_start_date': DateInput,
            'crawl_end_date': DateInput,
        }
    
    resource = forms.URLField(widget=ResourceInput, initial='http://')

    def __init__(self, *args, editable=False, tabbed=False, instance=None,
                 **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        self.helper = FormHelper(self)
            
        if hasattr(self.instance, 'pk') and self.instance.pk is not None:
            form_title = HTML('<h2 class="mb-0">{% load jargon %}{% term "nomination" "upper" %}: {{project}}</h2>'),
            form_buttons_kwargs = {
                'confirm_title': 'Save changes',
                'confirm_text': 'Click the submit button to save changes to this nomination or click on cancel to return to Cobweb without adding the new project.',
            }
        else:
            form_title = HTML('<h2 class="mb-0">New {% load jargon %}{% term "nomination" "lower" %}</h2>')
            form_buttons_kwargs = {
                'confirm_title': 'Add new nomination',
                'confirm_text': 'Click the submit button to nominate this resource or click on cancel to return to Cobweb without adding the new project.',
            }

        if 'project' in self.initial:
            project = Project.objects.get(pk=self.initial['project'])
            proj_header = HTML(
                '{% load jargon cobweb_look %}<h3>{% term "project" "capitalize" %}: {{project|as_link}}</h3>',

            )
        else:
            proj_header = HTML('')
        
        if tabbed:
            self.helper.layout = info_tabs(
                InfoTab(title='About the nomination',
                        content=nomination_info(editable=editable)),
                InfoTab(title='About the resource',
                        content=resource_info(editable=editable)),
            )
        else:
            self.helper.layout = Layout(
                Div(
                    form_title,
                    proj_header,
                    css_class='px-3 pt-0 pb-2 w-100',
                ),

                Row(
                    Pane(
                        Row(Column(HTML('<h4>About the resource</h4>'))),
                        resource_info(editable=editable),
                        css_class='col-6',
                    ),

                    Pane(
                        Row(Column(HTML('<h4>About the nomination</h4>'))),
                        nomination_info(
                            editable=editable,
                            form_buttons_kwargs=form_buttons_kwargs,
                        ),
                        css_class='col-6',
                    ),
                    css_class='flex-grow-1',
                )
            )
        self.helper.form_class='h-100 d-flex flex-column pb-2'

    def clean_resource(self):
        url = self.cleaned_data.get("resource")
        if not url:
            raise forms.ValidationError("Please enter a URL.")
        else:
            return Resource.objects.get_or_create(url=url)[0]


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        # fields = ('nomination', 'organization', 'active', 'has_holding')
        fields = ('__all__')
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
            'crawl_start_date': DateInput,
            'crawl_end_date': DateInput,
        }

    def __init__(self, *args, editable=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            FormSection(Row(Column(HTML('<h4>Claim Information</h4>')))),
            FormSection(Row(Column(
                HTML("""{% load as_link from cobweb_look %}
                    <a class="col-form-label form-control-label" href="{{form.instance.nomination.get_absolute_url}}">Nomination:</a>
                    <br>Resource URL: {{form.instance.nomination.resource|as_link}}
                    <br>Project: {{form.instance.nomination.project|as_link}}
                """),
                Hidden('nomination', value=self.initial['nomination']),
            )), css_class='form-group'),
            FormSection(
                Row(Column(HField('organization', edit=editable))),
                Row(Column(Field('active', edit=editable), css_class='col-6'),
                    Column(Field('has_holding', edit=editable), css_class='col-6')),
            ),
            crawl_scope_fields(editable=editable),
            FORM_BUTTONS if editable else HTML(''),
        )
