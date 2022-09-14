from django.urls import path
from .views import *


urlpatterns = [
    path('add-material/', add_material, name='add_material'),
    path('report/', material_report, name='material_report'),
    path('materials/export/excel/', export_materials_xls, name='export_materials_xls'),
]