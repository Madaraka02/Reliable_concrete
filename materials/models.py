from django.db import models

# Create your models here.
class RawMaterial(models.Model):
    item_name = models.CharField(max_length=400, null=True)
    units_bought
    pass