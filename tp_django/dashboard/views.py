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
prompt = """Tu es une IA spécialisée dans la création narrative pour jeux de rôle et jeux vidéo. Génère un univers original et cohérent selon les consignes suivantes (en respectant des limites de 100 caractères pour chaque champ) :

1. **Génération de l’univers** : 
   - Décris brièvement un monde immersif avec une géographie unique, des factions, une histoire récente et ancienne, et des enjeux majeurs.
   - Le texte de l'univers doit faire moins de 100 caractères.


3. **Élaboration de 2 à 4 personnages** :
   Pour chaque personnage, indique :
   - Nom
   - Race
   - Description (doit être courte, moins de 100 caractères)

4. **Illustration de l’histoire** :
   Génère une illustration pour l'histoire du jeu, en utilisant un style visuel cohérent avec le genre et l'ambiance du jeu. L’image doit être générée et renvoyée sous forme d'URL.

Voici un format structuré en JSON, limite les caractères à 100 pour chaque champ et inclut un lien vers l’illustration :
pour l'illustration il ne doit pas dépasser les 100 characteres 
{
    game: {
        univers: "Le monde de X, ravagé par des guerres. Un royaume perdu sous des nuages éternels.",
        story: "Les héros doivent sauver un artefact ancien. Mais d'autres veulent le pouvoir.",
        perso: [{
            name: "Zora",
            race: "Humaine",
            description: "Messagère des terres oubliées, elle protège les secrets du passé."
        }],
        illustration: ""
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
        print(context)
        return render(request, 'index.html', context)

    def post(self, request):
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game_data = form.cleaned_data  # Récupère les données du formulaire
            
            # Générer un prompt plus spécifique à partir des données du formulaire (si nécessaire)
            custom_prompt = prompt + f"\n\nInformations sur le jeu : {game_data}"

            # Effectuer la requête à l'API OpenAI pour générer des éléments narratifs
            response = client.chat.completions.create(
                model="chatgpt-4o-latest",  # Utilise ici un modèle compatible
                messages=[
                    {"role": "system", "content": "Tu es une IA spécialisée dans la création narrative pour jeux de rôle et jeux vidéo."},
                    {"role": "user", "content": custom_prompt}
                ],
                max_completion_tokens=1000,
                response_format={"type": "json_object"}
            )

            # Récupérer le contenu généré pour les éléments narratifs
            generated_content = response.choices[0].message.content

            try:
                generated_data = json.loads(generated_content)
            except json.JSONDecodeError as e:
                print(f"Erreur de parsing JSON : {e}")
                print(f"Contenu généré : {generated_content}")
                return render(request, 'index.html', {'error': 'Erreur de parsing JSON'})

            # Générer une illustration via DALL·E pour l'histoire
            illustration = self.generate_illustration(generated_data)

            # Ajouter l'URL de l'illustration dans les données générées
            generated_data['game']['illustration'] = illustration

            # Ajouter l'ID de l'utilisateur connecté
            generated_data['game']['user'] = request.user.id

            # Passer les données analysées au serializer
            serializer = GameSerializer(data=generated_data['game'], context={'request': request})
            print(generated_data['game'])
            print(serializer.is_valid())
            print(serializer.error_messages)
            print(serializer.errors)
            if serializer.is_valid():
                game = serializer.save()  # Sauvegarde du jeu créé
                return render(request, 'index.html', {'games': game})
            else:
                # Afficher les erreurs de validation du serializer
                return render(request, 'index.html', {'error': 'Erreur de validation', 'details': serializer.errors})

        return render(request, 'index.html')

    def generate_illustration(self, generated_data):
        """
        Fonction pour générer une illustration pour l'histoire du jeu.
        """
        # Générer une illustration pour l'histoire
        story_prompt = f"Illustration de l'histoire : {generated_data['game']['story']}"
        return self.create_image_from_prompt(story_prompt)

    def create_image_from_prompt(self, prompt):
        """
        Fonction pour appeler l'API de génération d'images (comme DALL·E) et obtenir l'URL de l'image.
        """
        # Appel à l'API OpenAI pour générer une image
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url

