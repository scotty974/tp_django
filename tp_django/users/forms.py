from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        label="Se souvenir de moi"
    )

    class Meta:
        model = User
        fields = ("username", "password")
        help_texts = {
            "username": None,
            "password": None,
        }

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {
            "username": None,
            "email":None,
            "password1":None,
            "password2":None,
    }

class MandatoryPasswordChangeForm(PasswordChangeForm):
    pass
