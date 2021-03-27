from django.views.generic import ListView,DetailView,TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
import requests

def home(request):
    return render(request, 'pokedexwebsitev2/index.html')

def list(request):
    context = {}
    is_cached = ('pokedata' in request.session)
    pokemon = {}
    r = {}

    if not is_cached:
        try:
            req = requests.get('https://halenkamp-pokemonapi.herokuapp.com/api/pokemon', params=request.GET)
            r = req.json()
            request.session['pokedata'] = r
        except requests.exceptions.ConnectionError:
            return HttpResponse("<p>Connection Refused</p>")

    r = request.session['pokedata'].copy()

    for pokemon in r:
        pokemonid = int(pokemon['dexnum'])
        pokemon['dexinteger'] = pokemonid
        pokemonid = int(pokemon['id'])
        pokemon['mod5'] = ((pokemonid-1) % 5)

    context = {
        'pokemonlist': r,
    }
    return render(request,'pokedexwebsitev2/list.html', context)

def base(request, id):
    # bulbasaur, for unknown reasons, is having data corruption on the api side. rendering a static template for this choice only, as this is the only
    # issue as far as I can tell
    if id == 1:
        return render(request, 'pokedexwebsitev2/bulb.html')
    is_cached = ('individualdata' in request.session)
    if not is_cached:
        request.session['individualdata'] = {}
    else:
        if str(id) not in request.session['individualdata']:
            is_cached = False
    
    pokemon = {}

    if not is_cached:
        try:
            req = requests.get('https://halenkamp-pokemonapi.herokuapp.com/api/pokemon?id='+str(id), params=request.GET)
            r = req.json()
            request.session['individualdata'][str(id)] = r
        except requests.exceptions.ConnectionError:
            return HttpResponse("<p>Connection Refused</p>")
    previd = 0
    nextid = 0
    if id == 1: 
        previd = 973 
    else: 
        previd = id - 1
    if id == 973: 
        nextid = 1 
    else: 
        nextid = id + 1
    
    pokemon = request.session['individualdata'][str(id)].copy()

    pokemonid = int(pokemon['dexnum'])
    pokemon['dexinteger'] = pokemonid

    pokemon['description'] = pokemon['description'].replace("&eacute;","é")

    for ability in pokemon['possibleabilities']:
        try:
            if pokemon['ability1'] != None:
                try:
                    if pokemon['ability2'] != None:
                        pokemon['ability3'] = ability
                except:
                    pokemon['ability2'] = ability
        except:
            pokemon['ability1'] = ability

    bst = pokemon['stats']['basehp'] + pokemon['stats']['baseatk'] + pokemon['stats']['basedef'] + pokemon['stats']['basespatk'] + pokemon['stats']['basespdef'] + pokemon['stats']['basespeed']
    pokemon['bst'] = bst

    # ENSURE YOURE USING A COPY OF THE CACHE, DONT MAKE THE SAME MISTAKE

    for move in pokemon['possiblemoves']:
        if move['power'] == "0":
            move['power'] = "—"
        if move['accuracy'] == "—":
            move['accuracy'] = 0.0

        num = float(move['accuracy'])   
        if num != 0.0:
            move['accuracy'] = num*100
        else:
            move['accuracy'] = "—"

    context = {
        'previouspokemon': request.session['pokedata'][previd-1],
        'pokemon': pokemon,
        'nextpokemon': request.session['pokedata'][nextid-1]
    }

    return render(request, 'pokedexwebsitev2/base.html', context)
    
    