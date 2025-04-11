from django.db import models
from django.contrib.auth.models import User  # Import du modèle User

class Personnage(models.Model):
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')  # lien avec l'utilisateur
    univers = models.CharField(max_length=100)
    story = models.CharField(max_length=100)
    perso = models.ManyToManyField(Personnage)
    illustration = models.CharField(max_length=100)
    gamePicth = models.CharField(max_length=100)

    def __str__(self):
        return self.univers
