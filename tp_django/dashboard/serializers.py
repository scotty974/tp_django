from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Personnage

class PersonnageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnage
        fields = ['id', 'name', 'race', 'description']

class GameSerializer(serializers.ModelSerializer):
    perso = PersonnageSerializer(many=True)  # pour afficher les personnages liés
    user = serializers.ReadOnlyField(source='user.username')  # seulement en lecture

    class Meta:
        model = Game
        fields = ['id', 'user', 'univers', 'story', 'perso', 'illustration']
