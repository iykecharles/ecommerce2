from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["image"]

        
        
        
        
