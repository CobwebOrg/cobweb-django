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
                Field('status', edit=editable, wrapper_class='col-md-5'),
                Field('administrators', edit=editable, wrapper_class='col-md-7'),
                css_id='project-admin-row',
            ),

            Row(
                Field('nomination_policy', edit=editable, wrapper_class='col-md-5'),
                Column(
                    Field('nominators', edit=editable),
                    Field('nominator_blacklist', edit=editable, show=editable),
                    css_class='col-md-7'
                ),
                css_id='project-nomination-row',
            ),

            Row(Column(Field('tags', edit=editable))),

            FORM_BUTTONS if editable else HTML(''),
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

    def __init__(self, *args, editable=False, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        self.helper = FormHelper(self)

        if 'project' in self.initial:
            project = Project.objects.get(pk=self.initial['project'])
            proj_header = HTML(format_html(
                '<h2 class="mb-0"><small><a href="{}"> Project: {}</a></small></h2>',
                project.get_absolute_url(),
                str(project),
            ))
        else:
            proj_header = HTML('')
            
        if hasattr(self.instance, 'pk') and self.instance.pk is not None:
            nom_header = HTML(format_html('<h3>NOMINATION: {}</h3>',
                                          str(self.instance)))
        else:
            nom_header = HTML('<h3>NEW NOMINATION</h3>')
        
        self.helper.layout = Layout(
            Div(
                proj_header,
                nom_header,
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
                    crawl_scope_fields(editable=editable),
                    FORM_BUTTONS if editable else HTML(''),

                    HTML("""{% if table %}
                                <h5>Claims</h5>
                                {% load render_table from django_tables2 %}
                                {% render_table table %}
                            {% endif %}"""),
                    css_class='col-5',
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
        template_name = 'projects/claim_form.html'
        # fields = ('nomination', 'organization', 'active', 'has_holding')
        fields = ('nomination', 'organization')
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
            Div(Field('nomination'), css_class='d-none'),
            Row(Column(HTML("""{% load as_link from cobweb_look %}
                               Resource URL: {{form.instance.nomination.resource|as_link}}"""))),
            Row(Column(HTML('Project: {{form.instance.nomination.project}}'))),
            Row(Column(HField('organization', edit=editable))),
            # Row(Column(Field('active'), css_class='col-6'),
            #     Column(Field('has_holding'), css_class='col-6')),
            FORM_BUTTONS if editable else HTML(''),
        )
