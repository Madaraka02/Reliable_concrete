from django.urls import path
from .views import *


urlpatterns = [
    path('add-material/', add_material, name='add_material'),
    path('add-material-use/', add_material_use, name='add_material_use'),
    path('report/', material_report, name='material_report'),
    path('materials/export/excel/', export_materials_xls, name='export_materials_xls'),
    path('materials-usage/export/excel/', export_material_usage_xls, name='export_material_usage_xls'),
    path('<int:id>/update/', update_material, name='update_material'),
    path('<int:id>/usage/update/', update_material_use, name='update_material_use'),

]
