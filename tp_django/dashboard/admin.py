from django.contrib import admin
from .models import GameUniverse, Character, ConceptArt, MainStory, GamePitch
# Register your models here.
admin.site.register(GameUniverse)
admin.site.register(Character)
admin.site.register(ConceptArt)
admin.site.register(MainStory)
admin.site.register(GamePitch)