from django.db import models  # noqa F401
from datetime import datetime

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя покемона')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Имя покемона на англ.яз')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Имя покемона на япон.яз')
    photo = models.ImageField(upload_to='pokemons', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey("self", related_name='previous_evolutions', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Эволюционировал из')

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name='entities', on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(blank=True, null=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, null=True, verbose_name='Сила')
    defence = models.IntegerField(blank=True, null=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, null=True, verbose_name='Выносливость')

    def __str__(self):
        return self.pokemon.title