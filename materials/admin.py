from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(RawMaterial)
admin.site.register(RawMaterialUsage)

admin.site.register(TimeStampedMaterialUpdate)
