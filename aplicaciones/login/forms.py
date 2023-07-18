from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.db import models
from django import forms

class UsuarioNuevoForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.is_staff = True
    #     if commit:
    #         user.save()
    #     return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario',max_length=50, required=True)
    password = forms.CharField(label='Clave', max_length=100, required=True,widget=forms.PasswordInput)

from captcha.fields import CaptchaField

class CaptchaForm(forms.Form):
    captcha = CaptchaField()
    