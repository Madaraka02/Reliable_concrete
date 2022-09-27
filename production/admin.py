from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(CuringStock)
admin.site.register(ReadyForSaleStock)
admin.site.register(ProductMaterialConsumption)
admin.site.register(Moulding)
admin.site.register(SalesTimestamp)

