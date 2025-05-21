from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile  # Import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Use CustomUser instead of User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = Profile
        fields = ['phone', 'address']
        labels = {
            'phone': 'Phone Number',
            'address': 'Address',
        }