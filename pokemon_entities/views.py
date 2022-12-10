import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon
from .models import PokemonEntity
from django.utils.timezone import localtime
import pytz

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = PokemonEntity.objects.filter(appeared_at__lte=localtime(), disappeared_at__gte=localtime())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    pokemons_on_page = []
    pokemons_all = Pokemon.objects.all()
    for pokemon in pokemons_all:
        if pokemon.photo:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.photo.url,
                'title_ru': pokemon.title,
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
            })


    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entity = PokemonEntity.objects.get(id=int(pokemon_id), appeared_at__lte=localtime(), disappeared_at__gte=localtime())
    if pokemon_entity:   
        for pokemon_entity in pokemon_entity.pokemon.pokemon_entityes.all(): 
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
            )
        one_pokemon = Pokemon.objects.get(id=int(pokemon_id))
        pokemon = {} 
        pokemon['pokemon_id']=int(pokemon_id)
        pokemon['title_ru']=one_pokemon.title
        pokemon['title_en']=one_pokemon.title_en
        pokemon['title_jp']=one_pokemon.title_jp
        pokemon['description']=one_pokemon.description
        pokemon['img_url']=request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        if one_pokemon.previous_evolution:
            old_pokemon = Pokemon.objects.get(title=one_pokemon.previous_evolution)
            previous_pokemon = {}
            previous_pokemon['title_ru']=old_pokemon.title
            previous_pokemon['pokemon_id']=old_pokemon.id
            previous_pokemon['img_url']=old_pokemon.photo.url
            pokemon['previous_evolution']=previous_pokemon
        if one_pokemon.evolution.first():
            new_pokemon = Pokemon.objects.get(title=one_pokemon.evolution.first())
            next_pokemon = {}
            next_pokemon['title_ru']=new_pokemon.title
            next_pokemon['pokemon_id']=new_pokemon.id
            next_pokemon['img_url']=new_pokemon.photo.url
            pokemon['next_evolution']=next_pokemon
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
