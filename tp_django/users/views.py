from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.views import View
from .forms import LoginForm, SignupForm, MandatoryPasswordChangeForm
from .models import Profile
import datetime
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

# Dictionnaire global pour bloquer temporairement les comptes (à améliorer avec cache ou base)
login_attempts = {}


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=email, email=email, password=password)
            user.profile.pseudonyme = form.cleaned_data['pseudonyme']
            user.profile.avatar = form.cleaned_data['avatar']
            form.clean()
            user.profile.must_change_password = True
            user.profile.save()
            login(request, user)
            return redirect('change_password')
        else:
            messages.error(request, "Erreur lors de l'inscription.")
            return render(request, 'signup.html', {'form': form})
            


class LoginView(View):
    def get(self, request):
        check = self.check(request)
        if check['blocked']:
            return render(request, 'login_blocked.html', {'wait_time': check['cooldown']})
        
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        check = self.check(request)
        if check['blocked']:
            return render(request, 'login_blocked.html', {'wait_time': check.cooldown})
        
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            self.reset_login_attempts(check['ip'])
            if request.user.profile.must_change_password:
                return redirect('change_password')
            return redirect('profile')
        else:
            self.increment_login_attempts(check['ip'])
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
            return render(request, 'login.html', {'form': form})

    # Méthodes utilitaires
    def get_ip(self, request):
        return request.META.get('REMOTE_ADDR')

    def get_login_attempts(self, ip):
        cache_key = f'login_attempts_{ip}'
        attempts = cache.get(cache_key)
        if attempts is None:
            attempts = {'count': 0 }
            cache.set(cache_key, attempts)
        return attempts

    def set_login_attempts(self, ip, attempts):
        cache_key = f'login_attempts_{ip}'
        cache.set(cache_key, attempts, timeout=300)

    def reset_login_attempts(self, ip):
        cache_key = f'login_attempts_{ip}'
        cache.delete(cache_key)

    def increment_login_attempts(self, ip):
        attempts = self.get_login_attempts(ip)
        attempts['count'] += 1
        logger.warning(f"Échec de connexion pour IP {ip}. Tentative n°{attempts['count']}")
        
        if attempts['count'] >= 3:
            attempts['blocked_until'] = timezone.now() + datetime.timedelta(minutes=2)
            logger.warning(f"Compte bloqué pour IP {ip} après 3 tentatives échouées")
        
        self.set_login_attempts(ip, attempts)
        logger.info(f"Nouvel état du cache pour {ip}: {attempts}")

    def check(self, request):
        ip = self.get_ip(request)
        attempts = self.get_login_attempts(ip)
        if attempts['count'] > 3:
            return {
                'ip': ip,
                'blocked': True,
                'cooldown': 120
            }
        check_result = {
            'ip': ip,
            'blocked': False,
        }
        print(f"check_result: {check_result}")
        return check_result

    def get_wait_time(self, ip):
        attempts = self.get_login_attempts(ip)
        return int((attempts['cooldown'] - timezone.now()).total_seconds() // 1)

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
