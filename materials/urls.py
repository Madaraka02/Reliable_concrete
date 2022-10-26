from django.urls import path
from .views import *


urlpatterns = [
    path('add-material/', add_material, name='add_material'),
    path('branch/<str:id>/sale/', branch_material_sale, name='branch_material_sale'),
    path('main/<str:id>/sale/', main_material_sale, name='main_material_sale'),
    path('dispatch/material/branch/', dispatch_material_to_branch, name='dispatch_material_to_branch'),
    path('dispatch/material/site/', dispatch_material_to_site, name='dispatch_material_to_site'),
    path('site/<str:id>/use/', site_material_use, name='site_material_use'),

    path('add-material-use/', add_material_use, name='add_material_use'),
    path('report/', material_report, name='material_report'),
    path('materials/export/excel/', export_materials_xls, name='export_materials_xls'),
    path('materials-usage/export/excel/', export_material_usage_xls, name='export_material_usage_xls'),
    path('<int:id>/update/', update_material, name='update_material'),
    path('<int:id>/usage/update/', update_material_use, name='update_material_use'),
    path('<int:id>/confirm-recceive/', confirm_material_receive, name='confirm_material_receive')

]

