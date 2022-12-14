from django.db import models
from production.models import *
from materials.models import *

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


class TDamage(models.Model):
    product = models.CharField(max_length=300, null=True)
    image =  models.FileField(upload_to='damages', null=True, blank=True)
    quantity_damaged = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    category = models.CharField(null=True, max_length=20, blank=True)
    date = models.DateField(null=True)

class Damage(models.Model):
    product = models.ForeignKey(Moulding, on_delete=models.CASCADE)
    image =  models.FileField(upload_to='damages', null=True, blank=True)
    quantity_damaged = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    category = models.CharField(null=True, max_length=20, blank=True)
    reason_for_damage = models.TextField(null=True, blank=True)
    date = models.DateField(null=True)
    


    def __str__(self):
        return f'Damages for {self.product.product.product.name}'       


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
    D8 = models.DecimalField(max_digits=20,decimal_places=2,default=0)

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
    D8 = models.DecimalField(max_digits=20,decimal_places=2,default=0)

    date = models.DateField(null=True)

    def __str__(self):
        return self.product.product.product.name        


class StockRecording(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)     
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    category = models.CharField(null=True, max_length=20, blank=True)
    extra_field_one = models.CharField(max_length=300, null=True, blank=True)     
    extra_field_two = models.CharField(max_length=300, null=True, blank=True)     
    extra_field_three = models.CharField(max_length=300, null=True, blank=True)     
    extra_field_four = models.CharField(max_length=300, null=True, blank=True)     
    extra_field_five = models.CharField(max_length=300, null=True, blank=True)     
    date = models.DateField(null=True) 

    def __str__(self):
        return str(self.name)  



class StockCounts(models.Model):
    product = models.ForeignKey(ProductMaterialConsumption, on_delete=models.CASCADE,null=True)
    quantity = models.DecimalField(max_digits=200,decimal_places=3, null=True,default=0)
    date = models.DateField(null=True) 


    def __str__(self):
        return str(self.product.product.name)  


class DispatchStockToBranch(models.Model):
    product = models.ForeignKey(ReadyForSaleStock, on_delete=models.CASCADE) 
    to = models.ForeignKey(Branch, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField(null=True)


    def __str__(self):
        return str(self.quantity)

class DispatchStockToSite(models.Model):
    product = models.ForeignKey(ReadyForSaleStock, on_delete=models.CASCADE) 
    to = models.ForeignKey(Site, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField(null=True)


    def __str__(self):
        return str(self.quantity)


class BranchStockCounts(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True) 
    product = models.ForeignKey(ReadyForSaleStock, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=200,decimal_places=3, null=True,default=0)
    date = models.DateField(null=True) 

    def __str__(self):
        return self.branch.name        


class SiteStockCounts(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True) 
    product = models.ForeignKey(ReadyForSaleStock, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=200,decimal_places=3, null=True,default=0)
    date = models.DateField(null=True) 

    def __str__(self):
        return self.site.name  


class BranchStockSale(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True) 
    product = models.ForeignKey(ReadyForSaleStock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    amount = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateField(null=True)


    def __str__(self):
        return str(self.quantity)

class SiteStockUse(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True) 
    product = models.ForeignKey(ReadyForSaleStock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField(null=True)


    def __str__(self):
        return str(self.quantity)        