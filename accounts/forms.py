from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="প্রথম নাম", required=False)
    last_name = forms.CharField(label="শেষ নাম", required=False)
    email = forms.EmailField(label="ইমেইল", required=True)

    class Meta:
        model = Profile
        fields = ['phone', 'address']
        labels = {
            'phone': 'ফোন নম্বর',
            'address': 'ঠিকানা',
        }