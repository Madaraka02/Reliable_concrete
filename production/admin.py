from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(CuringStock)
admin.site.register(ReadyStock)
admin.site.register(ProductMaterialConsumption)
admin.site.register(Moulding)

