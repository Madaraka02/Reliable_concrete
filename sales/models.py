from django.db import models
from production.models import Product

# Create your models here.
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    price_per_unit = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    client = models.CharField(max_length=300,null=True)
    order_number = models.CharField(max_length=500,null=True)
    date = models.DateField(null=True)

    @property
    def total_sale_price(self):
        total_sale_price = self.quantity * self.price_per_unit
        return total_sale_price


    def __str__(self):
        return f'Sale for {self.quantity} of {self.product}'