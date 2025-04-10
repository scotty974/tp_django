from django.db import models
from django.contrib.auth.models import User

class GameUniverse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='universes')
    
    TYPE_CHOICES = [
        ('RPG', 'RPG'),
        ('FPS', 'FPS'),
        ('Platformer', 'Platformer'),
        ('Adventure', 'Adventure'),
        ('Horror', 'Horror'),
        ('Other', 'Other'),
    ]
    title = models.CharField(max_length=100)
    game_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    ambiance = models.TextField()
    graphic_style = models.TextField()

    def __str__(self):
        return self.title

class MainStory(models.Model):
    universe = models.OneToOneField(GameUniverse, on_delete=models.CASCADE, related_name='story')
    title = models.CharField(max_length=100)
    synopsis = models.TextField()
    structure = models.TextField(help_text="Décris ici les arcs narratifs, les chapitres, les rebondissements...")

    def __str__(self):
        return f"Histoire de {self.universe.title}"

class Character(models.Model):
    universe = models.ForeignKey(GameUniverse, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    abilities = models.TextField()
    motivation = models.TextField()

    def __str__(self):
        return self.name

class ConceptArt(models.Model):
    universe = models.ForeignKey(GameUniverse, on_delete=models.CASCADE, related_name='concept_arts')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='concepts/')

    def __str__(self):
        return self.title

class GamePitch(models.Model):
    universe = models.OneToOneField(GameUniverse, on_delete=models.CASCADE, related_name='pitch')
    summary = models.TextField()
    target_audience = models.CharField(max_length=200)
    gameplay_mechanics = models.TextField()
    platforms = models.CharField(max_length=200)
    business_model = models.CharField(max_length=200)
    estimated_budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pitch de {self.universe.title}"
