from copy import deepcopy

import haystack.forms
from crispy_forms.helper import FormHelper
from dal import autocomplete
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, CharField, inlineformset_factory, Form, HiddenInput
from django.forms.models import model_to_dict

from core.layout import *
from core.models import User, Organization, Resource


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Field('username', edit=True),
                Field('password', edit=True),
                Div(
                    HTML("""
                        <a href="{% url 'password_reset' %}">(Lost password?)</a>
                    """),
                    FormActions(
                        Reset('reset', 'Cancel',
                              css_class='btn btn-light btn-outline-dark mr-1'),
                        Submit('submit', 'Submit', css_class='btn btn-primary'),
                        css_class='ml-auto',
                    ),
                    css_class='d-flex flex-row align-items-end'
                ),
                css_class='mt-5',
            ),
        )


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, edit=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Column(HTML('<h1>Sign up for a new user account</h1>'), css_class='col-12')),
            Row(
                Column(
                    Field('first_name', edit=edit),
                    Field('last_name', edit=edit),
                    Field('email', edit=edit),
                    # HTML('[[TERMS OF USE]]'),
                    css_class='col-6',
                ),
                Column(
                    Field('username', edit=edit),
                    Field('password1', edit=edit),
                    Field('password2', edit=edit),

                    FORM_BUTTONS,
                    css_class='col-6',
                )
            )
        )


class UserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'url',
                  'organization', 'professional_title']

    def __init__(self, *args, editable=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            HTML('<h2>User profile: {{object.username}}</h2>'),
            Row(
                Pane(
                    Field('first_name', edit=editable),
                    Field('last_name', edit=editable),
                    Field('email', edit=editable),
                    Field('url', edit=editable),
                    css_class='col-6',
                ),
                Pane(
                    Field('organization', edit=editable),
                    Field('professional_title', edit=editable),
                    form_buttons(
                        confirm_text='Click the submit button to save changes to you user profile or click on cancel to return to Cobweb without saving.',
                    ) if editable else HTML(''),
                    css_class='col-6',
                ),
                css_class='flex-grow-1',
            ),
        )
        self.helper.form_class = 'h-100 d-flex flex-column pb-2'


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['slug', 'full_name', 'short_name', 'administrators',
                  'parent_organization', 'description', 'address',
                  'telephone_number', 'url', 'email_address', 'contact']
        widgets = {
            'administrators': autocomplete.ModelSelect2Multiple(
                url='user_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
            'contact': autocomplete.ModelSelect2(
                url='user_autocomplete',
                attrs={'data-allow-clear': 'false'},
            ),
        }

    def __init__(self, *args, editable=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if hasattr(self.instance, 'pk') and self.instance.pk is not None:
            new = False
            slug_field = HTML("""
                <div id="div_slug" class="row form-group">
                    <label for="id_url" class="col-md-2 col-form-label form-control-label">
                        URL
                    </label>
                    <input type="text" name="slug" maxlength="50" id="id_slug"
                        class="textinput textInput form-control" hidden
                        value="{{organization.slug}}">
                    <div class="col-md w-100">
                        <div class="input-group">
                            <input type="text" name="slug" maxlength="50" id="id_url"
                                class="textinput textInput form-control" disabled
                                value="http://cobwebarchive.org{{organization.get_absolute_url}}">
                        </div>
                    </div>
                </div>
            """)
            form_title = HTML('<h2>Organization: {{organization}}</h2>')
            form_buttons_kwargs = {
                'confirm_title': 'Save changes',
                'confirm_text': 'Click the submit button to save changes to this organization or click on cancel to return to Cobweb without saving.',
            }
        else:
            new = True
            self.fields['slug'].label = "Choose a Cobweb URL"
            slug_field = HTML("""
                <div id="div_id_slug row" class="form-group">
                    <label for="id_slug" class="col-3 col-form-label requiredField">
                        Cobweb URL<span class="asteriskField">*</span>
                    </label>
                    <div class="col">
                        {% include 'bootstrap4/layout/form_help_toggler.html' %}
                        <span class="input-group">
                            <span class="input-group-prepend">
                                <span class="input-group-text">
                                    http://cobwebarchive.org/org/
                                </span>
                            </span>
                            <input type="text" name="slug" maxlength="50"
                                class="textinput textInput form-control"
                                required="" id="id_slug">
                        </span>
                        {% include 'bootstrap4/layout/help_text_and_errors.html' %}
                    </div>
                </div>
            """)
            form_title = HTML('<h2>New organization</h2>')
            form_buttons_kwargs = {
                'confirm_title': 'Save new organization',
                'confirm_text': 'Click the submit button to create this organization or click on cancel to return to Cobweb without saving.',
            }

        self.helper.layout = Layout(
            Div(
                form_title,
                css_class='px-3 pt-0 pb-2 w-100',
            ),
            Row(
                Pane(
                    slug_field,
                    HField('full_name', edit=editable),
                    HField('short_name', edit=editable),
                    HField('administrators', edit=editable),
                    HField('parent_organization', edit=editable),
                    HField('description', edit=editable),
                    css_class='col-6'
                ),
                Pane(
                    HField('address', edit=editable),
                    HField('telephone_number', edit=editable),
                    HField('url', edit=editable),
                    HField('email_address', edit=editable),
                    HField('contact', edit=editable),
                    # HField('identifier', edit=editable),
                    form_buttons(**form_buttons_kwargs) if editable else HTML(''),
                    css_class='col-6'
                ),
            ),
        )

        self.helper.help_text_inline = False


class SearchForm(haystack.forms.SearchForm):
    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            sqs = self.searchqueryset
            # return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
