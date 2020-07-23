from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_enabled = models.BooleanField()
    units_sold = models.PositiveIntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient)
    category_choices = [
        ('Bebida', 'Bebidas'),
        ('Hamburguesa', 'Hamburgesas'),
        ('Torta', 'Tortas'),
        ('Postre', 'Postres'),
    ]
    category = models.CharField(max_length=50, choices=category_choices)
    img = models.ImageField(blank=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('main:detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'
