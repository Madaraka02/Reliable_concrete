from django.db import models
from decimal import *

# Create your models here.

oil_price = Decimal(45)
diesel_price = Decimal(139.8)
half_ballast_price_per_kg = Decimal(1.25)
quarter_ballast_price_per_kg = 0
sand_price_per_kg = Decimal(0.4)
cement_price_per_kg = Decimal(13)
cement_price_bag = Decimal(650)
white_cement_price_per_kg = Decimal(13)
white_cement_price_bag = Decimal(650)
river_sand_price_per_kg = 0
dust_price_per_kg= 0
class Product(models.Model):
    name = models.CharField(max_length=400,null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class Production(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    target_production = models.IntegerField(null=True)
    actual_production = models.IntegerField(null=True)
    number_of_labourers = models.IntegerField(null=True)
    wage_per_labourer = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    oil_used_in_litres = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    fuel_used_in_litres = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    cement_bags_used = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    white_cement_bags_used = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    sand_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    river_sand_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    quarter_ballast_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    half_ballast_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    dust_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    damages = models.IntegerField(null=True)
    date = models.DateField(null=True)

    
    @property
    def sand_kgs(self):
        sand_kgs = self.sand_buckets_used * 28
        return sand_kgs

    @property
    def curing_number(self):
        curing_number = self.actual_production - self.damages
        return curing_number

    @property
    def river_sand_kgs(self):
        river_sand_kgs = self.river_sand_buckets_used * 35
        return river_sand_kgs

    @property
    def quarter_ballast_kgs(self):
        quarter_ballast_kgs = self.quarter_ballast_buckets_used * 30
        return quarter_ballast_kgs

    @property
    def half_ballast_kgs(self):
        half_ballast_kgs = self.half_ballast_buckets_used * 33
        return half_ballast_kgs

    @property
    def dust_kgs(self):
        dust_kgs = self.dust_buckets_used * 40
        return dust_kgs  

    @property
    def cement_kgs(self):
        cement_kgs = self.cement_bags_used * 50
        return cement_kgs 

    @property
    def white_cement_kgs(self):
        white_cement_kgs = self.white_cement_bags_used * 50
        return white_cement_kgs

    @property
    def total_wages(self):
        total_wages = self.number_of_labourers * self.wage_per_labourer
        return total_wages  


    @property
    def production_defeicit(self):
        production_defeicit=0  
        if self.target_production > self.actual_production:
            production_defeicit = self.target_production - self.actual_production
          
        return production_defeicit  



    @property
    def oil_cost(self):
        oil_cost = self.oil_used_in_litres * oil_price
        return oil_cost
        

    @property
    def cement_cost(self):
        cement_cost = self.cement_kgs * cement_price_per_kg
        return cement_cost
        

    @property
    def white_cement_cost(self):
        white_cement_cost = self.white_cement_kgs * white_cement_price_per_kg
        return white_cement_cost
        

    @property
    def sand_cost(self):

        sand_cost = self.sand_kgs * sand_price_per_kg
        return sand_cost
        


    @property
    def river_sand_cost(self):
        river_sand_cost = self.river_sand_kgs * river_sand_price_per_kg
        return river_sand_cost
        


    @property
    def quarter_ballast_cost(self):
        quarter_ballast_cost = self.quarter_ballast_kgs * quarter_ballast_price_per_kg
        return quarter_ballast_cost
        


    @property
    def half_ballast_cost(self):
        half_ballast_cost = self.half_ballast_kgs * half_ballast_price_per_kg
        return half_ballast_cost
        

    @property
    def dust_cost(self):
        dust_cost = self.dust_kgs * dust_price_per_kg
        return dust_cost
        

    @property
    def diesel_cost(self):
        diesel_cost = self.fuel_used_in_litres * diesel_price
        return diesel_cost
        

    @property
    def production_cost(self):
        production_cost = self.total_wages + self.oil_cost + self.cement_cost + self.white_cement_cost + self.sand_cost + self.river_sand_cost + self.quarter_ballast_cost + self.half_ballast_cost + self.dust_cost + self.diesel_cost
        return production_cost
        

    @property
    def day_total_production_income(self):
        day_total_production_income 
        return day_total_production_income
        pass
        
    def __str__(self):
        return f'production for {self.product.name} on {self.date}'

