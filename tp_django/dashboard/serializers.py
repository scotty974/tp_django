from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Personnage

class PersonnageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnage
        fields = ['id', 'game_id', 'name', 'race', 'description'] 

class GameSerializer(serializers.ModelSerializer):
    perso = PersonnageSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.id')  # Seulement en lecture

    class Meta:
        model = Game
        fields = ['id', 'user', 'univers', 'story', 'perso', 'illustration']

    def create(self, validated_data):
        personnages_data = validated_data.pop('perso', [])
        user = self.context['request'].user  # Récupère l'utilisateur depuis la requête

        # Créer le jeu avec l'utilisateur
        game = Game.objects.create(user=user, **validated_data)

        # Créer les personnages associés
        for personnage_data in personnages_data:
            Personnage.objects.create(game=game, **personnage_data)

        return game

