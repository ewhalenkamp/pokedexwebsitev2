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
            req = requests.get('http://127.0.0.1:8080/api/pokemon', params=request.GET)
            request.session['pokedata'] = req.json()
        except requests.exceptions.ConnectionError:
            return HttpResponse("<p>Connection Refused</p>")

    r = request.session['pokedata']
    for pokemon in r:
        print(pokemon['name'])

    context = {
        'pokemonlist': r,
    }
    return render(request,'pokedexwebsitev2/list.html', context)
    
    