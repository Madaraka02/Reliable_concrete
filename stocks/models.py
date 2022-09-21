from django.db import models
from production.models import *

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

DAMAGES_CHOICES = (
    ('PRODUCTION','PRODUCTION'),
    ('PACKING','PACKING'),
    ('CURING','CURING'),
    ('TRANSPORTING','TRANSPORTING'),
    ("OFFLOADING",'OFFLOADING'),
    )



class Damage(models.Model):
    product = models.ForeignKey(Moulding, on_delete=models.CASCADE)
    quantity_damaged = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    category = models.CharField(null=True, max_length=20, blank=True)
    date = models.DateField(null=True)
    image =  models.FileField(upload_to='damages', default='')


    def __str__(self):
        return f'Damages for {self.item.name}'       


# class History(models.models):
class ReleaseQty(models.Model):
    product = models.ForeignKey(Moulding, on_delete=models.CASCADE,null=True)
    oil = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    diesel = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    cement = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    white_cement = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    sand = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    river_sand = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    quarter_ballast = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    half_ballast = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    pumice = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    dust = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    date = models.DateField(null=True)

    def __str__(self):
        return self.product.product.name


class SemiReleaseQty(models.Model):
    product = models.ForeignKey(Moulding, on_delete=models.CASCADE,null=True)
    oil = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    diesel = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    cement = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    white_cement = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    sand = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    river_sand = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    quarter_ballast = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    half_ballast = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    pumice = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    dust = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    date = models.DateField(null=True)

    def __str__(self):
        return self.product.product.product.name        