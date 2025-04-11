from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import LoginForm, SignupForm
import logging
from rest_framework.views import APIView
from .serializers import (
    LoginSerializer, 
    SignupSerializer, 
)

logger = logging.getLogger(__name__)

class LoginView(APIView):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        serializer = LoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = authenticate(
                request=request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                return redirect('login')
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
        else:
            messages.error(request, "Erreur de valRidation.")
        return render(request, 'login.html', {'form': LoginForm()})

class SignupView(APIView):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        serializer = SignupSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return redirect('login')
        messages.error(request, "Erreur lors de l'inscription.")
        return render(request, 'signup.html', {'form': SignupForm()})

def logout_view(request):
    logout(request)
    return redirect('login')