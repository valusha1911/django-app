'''
Abs forms
'''
from django import forms
# from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from absUser.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'age', 'email', 'password1', 'password2', )
