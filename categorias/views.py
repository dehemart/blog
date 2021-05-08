from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Categoria


class CategoriaNav(ListView):
    model = Categoria
    context_object_name = 'categorias'
