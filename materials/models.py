from django.db import models
from production.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class RawMaterial(models.Model):
    name = models.CharField(max_length=400, null=True)
    confirm_received = models.BooleanField(default=False) #gramuel
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







class Branch(models.Model):
    name = models.CharField(max_length=400, null=True)
    manager = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=400, null=True)
    manager = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class DispatchMaterialExternal(models.Model): #to branch
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE) 
    to = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True) 
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField(null=True)


    def __str__(self):
        return self.to.name

class DispatchMaterialToSite(models.Model):
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE) 
    to = models.ForeignKey(Site, on_delete=models.CASCADE, null=True) 
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField(null=True)


    def __str__(self):
        return self.to.name


class MaterialCounts(models.Model):
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=200,decimal_places=3, null=True,default=0)
    date = models.DateField(null=True) 

    def __str__(self):
        return self.material.name


class BranchMaterialCounts(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True) 
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=200,decimal_places=3, null=True,default=0)
    date = models.DateField(null=True) 

    def __str__(self):
        return self.branch.name        


class SiteMaterialCounts(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True) 
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=200,decimal_places=3, null=True,default=0)
    date = models.DateField(null=True) 

    def __str__(self):
        return self.site.name   


class TotalMaterialCounts(models.Model): 
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=200,decimal_places=3, null=True,default=0)
 

    def __str__(self):
        return self.material.name          



class BranchMaterialSale(models.Model): 
    material = models.ForeignKey(BranchMaterialCounts, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=20,decimal_places=2, null=True)

    date = models.DateField(null=True)


    def __str__(self):
        return str(self.material.name)


class MaterialSale(models.Model): 
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    sale_by = models.CharField(max_length=400, null=True)
    date = models.DateField(null=True)


    def __str__(self):
        return str(self.material.name)


class SiteMaterialUse(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True) 
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE) 
    quantity = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    date = models.DateField(null=True)


    def __str__(self):
        return str(self.material.name)

