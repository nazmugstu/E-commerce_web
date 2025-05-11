from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # অথবা CustomUser আমদানি করুন

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # অথবা CustomUser
        fields = ['username', 'email', 'password1', 'password2']