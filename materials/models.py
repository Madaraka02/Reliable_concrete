from django.db import models

# Create your models here.
class RawMaterial(models.Model):
    name = models.CharField(max_length=400, null=True)
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True) #1000
    amount = models.DecimalField(max_digits=20,decimal_places=2, null=True) #400
    date = models.DateField(null=True)

    @property
    def price_per_unit(self):
        price_per_unit = self.amount /self.quantity
        return price_per_unit
        pass

    def __str__(self):
        return self.name

