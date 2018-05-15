from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from core.layout import (Layout, Column, Row, CancelButton, Submit, Field, FormActions, Fieldset,
                         UneditableField, HTML, Hidden, Reset, Div)
from core.models import User


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Field('username'),
                Field('password'),
                FormActions(
                    Reset('reset', 'Reset'),
                    Submit('submit', 'Submit'),
                    css_class='float-right',
                ),
                css_class='mt-5'
            ),
        )


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(Column(HTML('<h1>Sign up for a new user account</h1>'), css_class='col-12')),
            Row(
                Column(
                    Field('first_name'),
                    Field('last_name'),
                    Field('email'),
                    HTML('[[TERMS OF USE]]'),
                    css_class='col-6',
                ),
                Column(
                    Field('username'),
                    Field('password1'),
                    Field('password2'),

                    FormActions(
                        CancelButton,
                        Submit('submit', 'Submit'),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # import pdb; pdb.set_trace()

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('<h3>User: {{object.username}}</h3>'),
            Field('username'),

            Fieldset('Personal Information',
                     Field('first_name'),
                     Field('last_name'),
                     Field('email'),
                     Field('url'),
                     ),

            Field('affiliations'),

            Fieldset('Preferences',
                     Field('get_notification_emails'),
                     ),

            FormActions(
                CancelButton,
                Submit('submit', 'Submit'),
                css_class='float-right'
            ),
        )
