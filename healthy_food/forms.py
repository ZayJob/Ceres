from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('url', 'company', 'address', 'phone')


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')