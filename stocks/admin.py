from django.contrib import admin
from .models import *
from production.models import Production
# Register your models here.
admin.site.register(Stock)
admin.site.register(ReleaseQty)

admin.site.register(Production)
