from django.shortcuts import render
from .models import Dish
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'main/index.html'
    context_object_name = 'dishes_list'

    def get_queryset(self):
        """Return the dishes"""
        return Dish.objects.all()