from django import forms
from .models import Game
class CreateGameForm(forms.Form):
    gameGenre = forms.CharField(max_length=100)
    atmosphere = forms.CharField(max_length=100)
    keywords = forms.CharField(max_length=100)
    ref = forms.CharField(max_length=100)
    
    class Meta:
        model = Game
        fields = ['gameGenre', 'atmosphere', 'keywords', 'ref']