from django.db import models
from production.models import *

# Create your models here.
SALE_CHOICES = (
    ('PRODUCTION','PRODUCTION'),
    ('PACKING','PACKING'),
    ('CURING','CURING'),
    ('TRANSPORTING','TRANSPORTING'),
    ("OFFLOADING",'OFFLOADING'),
    )
class Sale(models.Model):
    product = models.ForeignKey(ReadyForSaleStock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    price_per_unit = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    order_type = models.CharField(null=True, choices=SALE_CHOICES, max_length=30)
    order_documents = models.FileField(upload_to='orders', default=True)
    date = models.DateField(null=True)

    @property
    def total_sale_price(self):
        total_sale_price = self.quantity * self.price_per_unit
        return total_sale_price


    def __str__(self):
        return f'Sale for {self.quantity} of {self.product}'