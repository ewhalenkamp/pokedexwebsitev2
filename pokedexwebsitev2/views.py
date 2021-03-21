from django.views.generic import ListView,DetailView,TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
import requests

def home(request):
    return render(request, 'pokedexwebsitev2/index.html')

def list(request):
    r = requests.get('http://localhost:8080/api/pokemon', params=request.GET)
    #print(r.text)
    return render(request,'pokedexwebsitev2/list.html')