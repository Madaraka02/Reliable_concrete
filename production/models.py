from django.db import models
from decimal import *
# from materials.models import RawMaterial
from datetime import datetime, date, timedelta
# Create your models here.

current_date = datetime.today()

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

# what are you producing? Kabro Nyota quantity - the system checks how many
# per unit
# eg kabro 1sqM
class ProductMaterialConsumption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
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
    curing_days = models.PositiveIntegerField(default=10)

        
    
    def __str__(self):
        return self.product.name



# say 100sqM was produced : multiply for each material and then deduct from materials

class Moulding(models.Model):

    product = models.ForeignKey(ProductMaterialConsumption, on_delete=models.CASCADE, null=True)
    # target_production = models.IntegerField(null=True, blank=True)
    qty_to_be_produced = models.IntegerField(null=True, blank=True)
    number_of_labourers = models.IntegerField(null=True, blank=True)
    wage_per_labourer = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    transfered_to_curing = models.BooleanField(default=False)
    production_confirmed = models.BooleanField(default=False)
    date = models.DateField(null=True, blank=True)

    # @property
    # def oil_cost(self):
    #     oil_cost = self.oil_used_in_litres * oil_price
    #     return oil_cost

    # @property
    # def production_cost(self):
    #     production_cost = self.total_wages + self.oil_cost + self.cement_cost + self.white_cement_cost + self.sand_cost + self.river_sand_cost + self.quarter_ballast_cost + self.half_ballast_cost + self.dust_cost + self.diesel_cost
    #     return production_cost
        
    @property
    def oil_ltrs(self):
        oil_ltrs = self.product.oil * self.qty_to_be_produced
        return oil_ltrs

    @property
    def diesel_ltrs(self):
        diesel_ltrs = self.product.diesel * self.qty_to_be_produced
        return diesel_ltrs

    @property
    def cement_kgs(self):
        cement_kgs = self.product.cement * 50 * self.qty_to_be_produced
        return cement_kgs
    @property
    def pumice_kgs(self):
        pumice_kgs = self.product.pumice * self.qty_to_be_produced
        return pumice_kgs
    @property
    def white_cement_kgs(self):
        white_cement_kgs = self.product.white_cement * self.qty_to_be_produced
        return white_cement_kgs

    @property
    def sand_kgs(self):
        sand_kgs = self.product.sand * self.qty_to_be_produced
        return sand_kgs
    
    @property
    def rsand_kgs(self):
        rsand_kgs = self.product.river_sand * self.qty_to_be_produced
        return rsand_kgs

    @property
    def quarter_ballast_kgs(self):
        quarter_ballast_kgs = self.product.quarter_ballast * self.qty_to_be_produced
        return quarter_ballast_kgs

    @property
    def half_ballast_kgs(self):
        half_ballast_kgs = self.product.half_ballast * self.qty_to_be_produced
        return half_ballast_kgs

    @property
    def dust_kgs(self):
        dust_kgs = self.product.dust * self.qty_to_be_produced
        return dust_kgs

    def __str__(self):
        return self.product.product.name


class Production(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    target_production = models.IntegerField(null=True, blank=True)
    actual_production = models.IntegerField(null=True, blank=True)
    number_of_labourers = models.IntegerField(null=True, blank=True)
    wage_per_labourer = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    
    oil_used_in_litres = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    fuel_used_in_litres = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    cement_bags_used = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    white_cement_bags_used = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    sand_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    river_sand_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    quarter_ballast_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    half_ballast_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    dust_buckets_used = models.DecimalField(max_digits=20,decimal_places=2, null=True, blank=True)
    damages = models.IntegerField(null=True, blank=True)
    transfered_to_curing = models.BooleanField(default=False)
    date = models.DateField(null=True, blank=True)

    # def transfer(self):
    #     if self.transfered_to_curing==False:

    #         date_1 = datetime.strptime(self.date, '%m-%d-%Y')
    #         date_2 = date_1 + timedelta(days=1)
    #         if current_date == date_2:
    #             self.transfered_to_curing == True
    #             CuringStock.objects.create(product=self, enter_date=current_date,curing_days=3,transfered_to_ready=False)
                




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

class CuringStock(models.Model):
    product = models.ForeignKey(Moulding, on_delete=models.SET_NULL,null=True)
    enter_date = models.DateTimeField(auto_now_add=True)
    transfered_to_ready = models.BooleanField(default=False)


    # def transfer():
    #     current_date = datetime.today()
    #     date_1 = datetime.strptime(self.date, '%m-%d-%Y')
    #     date_2 = date_1 + timedelta(days=3)
    #     if current_date == date_2:
    #         self.transfered_to_ready == True


    def __str__(self):
        return self.product.product.product.name

class ReadyStock(models.Model):
    stock = models.ForeignKey(CuringStock, on_delete=models.SET_NULL, null=True) 
    sold = models.BooleanField(default=False)
    selling = models.BooleanField(default=False) 

    quantity_sold = models.IntegerField(default=0, null=True, blank=True)
    date_received = models.DateTimeField(auto_now_add=True, null=True)
    date_sold = models.DateField(null=True, blank=True)

    @property
    def remaining_stock(self):
        remaining_stock = self.stock.product.qty_to_be_produced - self.quantity_sold
        return remaining_stock

    def __str__(self):
        return self.sold  

class ReadyForSaleStock(models.Model):
    stock = models.ForeignKey(CuringStock, on_delete=models.SET_NULL, null=True) 
    sold = models.BooleanField(default=False)
    selling = models.BooleanField(default=False) 

    quantity_sold = models.IntegerField(default=0, null=True, blank=True)
    date_received = models.DateTimeField(auto_now_add=True, null=True)
    date_sold = models.DateField(null=True, blank=True)

    @property
    def remaining_stock(self):
        remaining_stock = self.stock.product.qty_to_be_produced - self.quantity_sold
        return remaining_stock

    def __str__(self):
        return self.stock.product.product.product.name 