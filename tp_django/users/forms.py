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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password'].label = "Mot de passe"
        
    def clean(self):
        cleaned_data = super().clean()
        
        if self.is_valid():
            remember_me = cleaned_data.get('remember_me', True)
            
            if remember_me:
                self.request.session.set_expiry(1209600)  # 2 semaines
            else:
                self.request.session.set_expiry(0)  # Session expire à la fermeture du navigateur
            
        return cleaned_data


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
