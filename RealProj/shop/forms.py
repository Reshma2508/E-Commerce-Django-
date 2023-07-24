from django import forms
from .models import Customer
from django.contrib.auth.models import User

class cform(forms.ModelForm):
    class Meta:
        model= Customer
        fields = '__all__'


class SignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['username','password','email']
        widgets = {
            'password': forms.PasswordInput
        }