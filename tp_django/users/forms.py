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

    def clean(self):
        cleaned_data = super().clean()
        print("Données nettoyées:", cleaned_data)
        return cleaned_data
    
    def save(self):
        user = super().save(commit=False)
        return user


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
        
    def save(self):
        user = super().save(commit=False)
        user.save()
        return user
        
    def clean(self):
        cleaned_data = super().clean()
        print("Données nettoyées:", cleaned_data)
        return cleaned_data




class MandatoryPasswordChangeForm(PasswordChangeForm):
    pass
