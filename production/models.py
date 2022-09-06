from django.db import models

# Create your models here.
class Production(models.Model):
    product = models.CharField(max_length=400,null=True)
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
    date = models.DateField()
    
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
    def total_wages(self):
        total_wages = self.number_of_labourers * self.wage_per_labourer
        return total_wages 

    @property
    def production_defeicit(self):
        if self.target_production > self.actual_production:
            production_defeicit = self.target_production * self.actual_production
        production_defeicit=0    
        return production_defeicit  

    @property
    def oil_cost(self):
        oil_cost = self.oil_used_in_litres * oil_price
        return oil_cost
        pass

    @property
    def diesel_cost(self):
        diesel_cost = self.fuel_used_in_litres * fuel_price
        return diesel_cost
        pass

    @property
    def day_total_production_cost(self):
        day_total_production_cost 
        return day_total_production_cost
        pass
        
    def __str__(self):
        return f'production for {self.product} on {self.date}'
