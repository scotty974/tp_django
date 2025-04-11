from django.urls import path
from .views import IndexView
urlpatterns = [
    path('dashboard/', IndexView.as_view(), name='dashboard'),
]