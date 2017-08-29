from django.forms import ModelForm

from . import models

class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = ['name', 'description']