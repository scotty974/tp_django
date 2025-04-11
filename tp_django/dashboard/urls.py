from django.urls import path
from .views import IndexView, GamePersonnagesView
urlpatterns = [
    path('dashboard/', IndexView.as_view(), name='dashboard'),
    path('games/<int:game_id>/personnages/', GamePersonnagesView.as_view(), name='game-personnages'),
]