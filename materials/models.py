from django.db import models
from production.models import ProductMaterialConsumption

# Create your models here.
class RawMaterial(models.Model):
    name = models.CharField(max_length=400, null=True)
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True) #1000
    amount = models.DecimalField(max_digits=20,decimal_places=2, null=True) #400
    date = models.DateField(null=True)

    available_qty = models.IntegerField(default=0, null=True, blank=True)

    # date_sold = models.DateField(null=True, blank=True)
    # quantity_used = models.IntegerField(default=0, null=True, blank=True)



    @property
    def price_per_unit(self):
        price_per_unit = self.amount /self.quantity
        return price_per_unit
        

    def __str__(self):
        return self.name


class TimeStampedMaterialUpdate(models.Model):
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    amount_paid = models.DecimalField(max_digits=20,decimal_places=2, null=True, default=0)
    date = models.DateField(null=True)

    def __str__(self):
        return self.material.name

class RawMaterialUsage(models.Model):
    material = models.ForeignKey(RawMaterial, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(ProductMaterialConsumption, on_delete=models.CASCADE, null=True)
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField(null=True)


    @property
    def remaining_quantity(self):
        remaining_quantity = self.material.quantity - self.quantity
        return remaining_quantity
        

    def __str__(self):
        return self.material

