from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

class IndexView(LoginRequiredMixin, View):
    redirect_field_name = 'next'  # paramètre GET utilisé par défaut

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        return render(request, 'index.html')
