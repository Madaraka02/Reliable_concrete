from django.db import models

# Create your models here.

CATEGORY_CHOICES = (
    ("Ready", "Ready"),
    ("Curring", "Curring")
)
class Stock(models.Model):
    name = models.CharField(max_length=300, null=True)    
    stage = models.CharField(max_length = 50,choices = CATEGORY_CHOICES,default = 'Ready')
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    price_per_unit = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField()

    @property
    def total(self):
        total = self.quantity * self.price_per_unit
        return total

    def __str__(self):
        return f'{self.name} in {self.stage} stage'