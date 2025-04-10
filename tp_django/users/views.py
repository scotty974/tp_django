from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.cache import cache
from django.views import View
from .forms import LoginForm, SignupForm, MandatoryPasswordChangeForm
import datetime
import logging

logger = logging.getLogger(__name__)

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Erreur lors de l'inscription.")
            return render(request, 'signup.html', {'form': form})
            
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            login(request, form.get_user())
            logger.info(f"Connexion réussie pour l'utilisateur {form.get_user().username}")
            return redirect('profile')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
            return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = MandatoryPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            profile = request.user.profile
            profile.must_change_password = False
            profile.save()
            messages.success(request, "Mot de passe changé avec succès.")
            return redirect('profile')
    else:
        form = MandatoryPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})
