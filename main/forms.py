from django import forms
from .models import Dish


class DishForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Dish
        fields = [
            'name',
            'description',
            'price',
            'is_enabled',
            'category',
            'units_sold',
            'img'
        ]
