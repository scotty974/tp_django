from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import CreateGameForm
from .models import Game, Personnage
from openai import OpenAI
from django.conf import settings
import json
from .serializers import GameSerializer

# Initialiser le client OpenAI avec la clé API
client = OpenAI()
client.api_key = settings.OPENAI_API_KEY

# Ton prompt
prompt = """Tu es une IA spécialisée dans la création narrative pour jeux de rôle et jeux vidéo. Génère un univers original et cohérent selon les consignes suivantes :

1. **Génération de l’univers** : 
   - Décris un monde immersif avec une géographie unique, des factions, une histoire récente et ancienne, et des enjeux majeurs.
   - Indique le genre (fantasy, post-apo, SF, etc.) et le ton (dramatique, sombre, épique, etc.).

2. **Création d’un scénario en 3 actes** :
   - Acte 1 : Présente les personnages, le monde et une situation de départ.
   - Acte 2 : Introduis un retournement narratif majeur qui bouleverse la mission initiale.
   - Acte 3 : Résolution dramatique (ouverte ou fermée).
   - Le scénario doit être structuré, rythmé, avec des conflits internes et externes.

3. **Élaboration de 2 à 4 personnages** :
   Pour chaque personnage, indique :
   - Nom
   - Classe ou type (ex: mercenaire, magicien, scientifique…)
   - Rôle narratif (héros, rival, mentor…)
   - Background personnel
   - Objectifs et relations avec les autres personnages
   - Style de gameplay associé (furtif, tank, contrôle mental, etc.)

4. **Création de lieux emblématiques** :
   - Décris au moins 3 lieux clés de l’univers avec des détails sensoriels (visuels, sonores, historiques).
   - Ces lieux doivent jouer un rôle narratif important.

Donne la réponse dans un format structuré en json pour faciliter son intégration dans un outil ou moteur de jeu, la structure doit respecter ce json ne modifie aucun champ, ne rajoute aucun champ, contente toi de remplir : 

{
    game:{
        univers:"",
        story: "",
        perso: [{
            name: "",
            race: "",
            description: ""
            }],
    }
}
"""

class IndexView(LoginRequiredMixin, View):
    redirect_field_name = 'next'

    def get(self, request):
        form = CreateGameForm()
        games = Game.objects.filter(user=request.user)
        context = {
            'form': form,
            'games': games
        }
        return render(request, 'index.html', context)

    def post(self, request):
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game_data = form.cleaned_data  # Récupère les données du formulaire
            
            # Générer un prompt plus spécifique à partir des données du formulaire (si nécessaire)
            custom_prompt = prompt + f"\n\nInformations sur le jeu : {game_data}"

            # Effectuer la requête à l'API OpenAI avec le format attendu (messages)
            response = client.chat.completions.create(
                model="chatgpt-4o-latest",  # Utilise ici un modèle compatible
                messages=[
                    {"role": "system", "content": "Tu es une IA spécialisée dans la création narrative pour jeux de rôle et jeux vidéo."},
                    {"role": "user", "content": custom_prompt}
                ],
                max_completion_tokens=1000,
            )

            # Récupérer le contenu généré
            generated_content = response.choices[0].message.content
            print(generated_content)

            try:
                # Convertir le contenu JSON généré en dictionnaire Python
                generated_data = json.loads(generated_content)
            except json.JSONDecodeError:
                # Si le contenu généré n'est pas un JSON valide
                return render(request, 'index.html', {'error': 'Le contenu généré n\'est pas au format JSON valide.'})
            
            # Passer les données analysées au serializer
            serializer = GameSerializer(data=generated_data['game'], context={'request': request})
            if serializer.is_valid():
                print('caca')
                game = serializer.save()  # Sauvegarde du jeu créé
                return render(request, 'index.html', {'game': game})
            else:
                # Afficher les erreurs de validation du serializer
                print(serializer.errors)
                return render(request, 'index.html', {'error': 'Erreur de validation', 'details': serializer.errors})

        return render(request, 'index.html')
