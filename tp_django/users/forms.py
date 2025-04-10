from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.core.validators import BaseValidator, RegexValidator
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        label="Se souvenir de moi"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Email"
        self.fields['password'].label = "Mot de passe"
        
    def clean(self):
        cleaned_data = super().clean()
        remember_me = cleaned_data.get('remember_me')
        
        if remember_me:
            self.request.session.set_expiry(1209600)
        else:
            self.request.session.set_expiry(0)
            
        return cleaned_data


class SignupForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        min_length=8,
        help_text="Minimum 8 caractères"
    )
    pseudonyme = forms.CharField(
        label="Pseudonyme",
        min_length=3,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9_-]+$',
                'Le pseudonyme ne peut contenir que des lettres, chiffres, tirets et underscores'
            )
        ]
    )
    avatar = forms.ImageField(
        label="Avatar",
        required=False,
        help_text="Image de profil (optionnelle)"
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Créer le profil associé
            Profile.objects.create(
                user=user,
                pseudonyme=self.cleaned_data['pseudonyme'],
                avatar=self.cleaned_data.get('avatar')
            )
        return user


class MandatoryPasswordChangeForm(PasswordChangeForm):
    pass
