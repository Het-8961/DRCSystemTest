from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm

from .models import signUp

class SignUpForm(ModelForm):
    class Meta:
        model = signUp
        # Password = forms.CharField(widget=forms.PasswordInput)
        fields = [
            'userName', 'email', 'mobile','password'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }
