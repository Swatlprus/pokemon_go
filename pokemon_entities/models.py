from django.db import models  # noqa F401
from datetime import datetime

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_jp = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to='pokemons', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    previous_evolution = models.ForeignKey("self", related_name='evolution', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name='pokemon_entityes', on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=datetime.now)
    disappeared_at = models.DateTimeField(default=datetime.now)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0, blank=True, null=True)
    strength = models.IntegerField(default=0, blank=True, null=True)
    defence = models.IntegerField(default=0, blank=True, null=True)
    stamina = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.pokemon.title