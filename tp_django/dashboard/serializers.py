from rest_framework import serializers
from .models import GameUniverse, MainStory, Character, ConceptArt, GamePitch

class MainStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainStory
        fields = '__all__'

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

class ConceptArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptArt
        fields = '__all__'

class GamePitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePitch
        fields = '__all__'

class GameUniverseSerializer(serializers.ModelSerializer):
    story = MainStorySerializer(read_only=True)
    characters = CharacterSerializer(many=True, read_only=True)
    concept_arts = ConceptArtSerializer(many=True, read_only=True)
    pitch = GamePitchSerializer(read_only=True)

    class Meta:
        model = GameUniverse
        fields = '__all__'
