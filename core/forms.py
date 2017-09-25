from crispy_forms.helper import FormHelper
from crispy_forms import layout
from django.forms import EmailField
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    email = EmailField(required=True)
    # first_name
    # last_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(layout.Submit('submit', 'Submit'))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

