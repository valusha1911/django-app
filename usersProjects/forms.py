from django import forms
from django.forms import ModelForm

from .models import Project, Technology


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = '__all__'