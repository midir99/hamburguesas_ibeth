from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_enabled = models.BooleanField()
    units_sold = models.PositiveIntegerField(default=0)
    category_choices = [
        ('Bebida', 'Bebidas'),
        ('Hamburguesa', 'Hamburgesas'),
        ('Torta', 'Tortas'),
        ('Postre', 'Postres'),
    ]
    category = models.CharField(max_length=50, choices=category_choices)
    # img = models.ImageField()

    def __str__(self):
        return f'{self.name}'
