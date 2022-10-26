from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(RawMaterial)
admin.site.register(RawMaterialUsage)
admin.site.register(MaterialCounts)
admin.site.register(BranchMaterialCounts)
admin.site.register(DispatchMaterialExternal)
admin.site.register(DispatchMaterialToSite)
admin.site.register(SiteMaterialCounts)
admin.site.register(TimeStampedMaterialUpdate)
admin.site.register(MaterialSale)
admin.site.register(Branch)
admin.site.register(Site)
