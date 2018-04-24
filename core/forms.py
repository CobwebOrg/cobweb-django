from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm

from core.layout import (Layout, CancelButton, Submit, Field, FormActions, Fieldset,
                         UneditableField, HTML, Hidden)
from core.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('username'),
            Field('password1'),
            Field('password2'),

            FormActions(
                CancelButton,
                Submit('submit', 'Submit'),
                css_class='float-right'
            ),
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
