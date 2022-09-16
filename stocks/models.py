from django.db import models
from production.models import Product

# Create your models here.


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    Ready = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    Curing = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    damages = models.IntegerField(null=True)
    price_per_unit = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField(null=True)

    @property
    def total_price(self):
        total_units = self.Ready + self.Curing
        total_price = total_units * self.price_per_unit
        return total_price


    @property
    def total_in_stock(self):
        total_in_stock = self.Ready + self.Curing
        return total_in_stock

    def __str__(self):
        return self.name


class Damage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    packing = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    production = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    arranging = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    # quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField(null=True)


    def __str__(self):
        return f'Damages for {self.item.name}'       


# class History(models.models):
