import folium
from django.shortcuts import render
from .models import Pokemon
from .models import PokemonEntity
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


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
    current_time = localtime()
    pokemons = PokemonEntity.objects.filter(appeared_at__lte=current_time, disappeared_at__gte=current_time)
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
                'img_url': DEFAULT_IMAGE_URL,
                'title_ru': pokemon.title,
            })


    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    current_time = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = get_object_or_404(PokemonEntity, id=int(pokemon_id), appeared_at__lte=current_time, disappeared_at__gte=current_time).pokemon.entities.all()
    for pokemon_entity in pokemon_entities: 
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )
    one_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))
    pokemon = {
        'pokemon_id': int(pokemon_id),
        'title_ru': one_pokemon.title,
        'title_en': one_pokemon.title_en,
        'title_jp': one_pokemon.title_jp,
        'description': one_pokemon.description,
        'img_url': request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        } 
    if one_pokemon.previous_evolution is not None:
        old_pokemon = Pokemon.objects.get(title=one_pokemon.previous_evolution)
        context = {
        'pokemon_id': old_pokemon.id,
        'title_ru': old_pokemon.title,
        'img_url': old_pokemon.photo.url,
        }
        pokemon['previous_evolution']=context
    if one_pokemon.previous_evolutions.first():
        new_pokemon = Pokemon.objects.get(title=one_pokemon.previous_evolutions.first())
        context = {
        'pokemon_id': new_pokemon.id,
        'title_ru': new_pokemon.title,
        'img_url': new_pokemon.photo.url,
        }
        pokemon['next_evolution']=context

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
