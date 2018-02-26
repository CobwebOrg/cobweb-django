from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm

from core.layout import Layout, CancelButton, Submit, Field, FormActions
from core.models import User


class UserForm(UserCreationForm):

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
