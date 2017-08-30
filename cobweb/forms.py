from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, EmailField

from . import models

class UserForm(UserCreationForm):
    email = EmailField(required=True)
    # first_name
    # last_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    class Meta:
        model = auth.models.User
        fields = ("username", "email", "password1", "password2")

class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = models.Project
        fields = ['name', 'description']