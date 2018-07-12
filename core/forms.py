import haystack.forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from core.layout import (Layout, Column, Row, Submit, Field, FormActions,
                         FORM_BUTTONS, Fieldset, UneditableField, HTML,
                         Reset, Div)
from core.models import User


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Field('username', edit=True),
                Field('password', edit=True),
                FormActions(
                    Reset('reset', 'Reset', css_class='btn btn-light btn-outline-dark mr-1'),
                    Submit('submit', 'Submit', css_class='btn btn-info'),
                    css_class='float-right',
                ),
                css_class='mt-5',
            ),
        )


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

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
                    HTML('[[TERMS OF USE]]'),
                    css_class='col-6',
                ),
                Column(
                    Field('username', edit=edit),
                    Field('password1', edit=edit),
                    Field('password2', edit=edit),

                    FormActions(
                        Reset('reset', 'Reset', css_class='btn btn-light btn-outline-dark mr-1'),
                        Submit('submit', 'Submit', css_class='btn btn-info'),
                        css_class='float-right',
                    ),
                    css_class='col-6',
                )
            )
        )


class UserProfileForm(UserCreationForm):

    class Meta:
        model = User
        exclude = ()

    def __init__(self, *args, editable=True, **kwargs):
        super().__init__(*args, **kwargs)
        # import pdb; pdb.set_trace()

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('<h3>User: {{object.username}}</h3>'),
            Field('username', edit=edit),

            Fieldset('Personal Information',
                     Field('first_name', edit=edit),
                     Field('last_name', edit=edit),
                     Field('email', edit=edit),
                     Field('url', edit=edit),
                     ),

            Field('organization', edit=edit),
            Field('professional_title', edit=edit),

            Fieldset('Preferences',
                     Field('get_notification_emails', edit=edit),
                     ),

            FORM_BUTTONS if editable else HTML(''),
        )


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