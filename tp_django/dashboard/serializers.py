from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Personnage

class PersonnageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnage
        exclude = ['game_id']  # game_id sera injecté depuis GameSerializer

class GameSerializer(serializers.ModelSerializer):
    perso = PersonnageSerializer(many=True)

    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Game
        fields = ['id', 'user', 'univers', 'story', 'perso', 'illustration']

    def create(self, validated_data):
        personnages_data = validated_data.pop('perso', [])
        user = self.context['request'].user
        game = Game.objects.create(user=user, **validated_data)

        for personnage_data in personnages_data:
            Personnage.objects.create(game_id=game, **personnage_data)

        return game



