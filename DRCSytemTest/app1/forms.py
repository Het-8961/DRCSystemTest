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

class LoginForm(forms.Form):
    UserName = forms.CharField(max_length=20, required=False,help_text="Username or Mobile")
    Password = forms.CharField(widget=forms.PasswordInput, required=False)

class TwoFactAuth(forms.Form):
    # OTP = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}),required=True)
    OTP = forms.IntegerField(required=False)