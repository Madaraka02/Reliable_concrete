from django.urls import path
from .views import *


urlpatterns = [
    path('', production_post, name='production'),
    path('add-product/', add_product, name='add_product'),
    path('report/', production_report, name='production_report'),
    path('production/export/excel/', export_production_xls, name='export_production_xls'),
    path('products/<int:id>/update/', update_product, name='update_product'),
    path('<int:id>/update/', update_production, name='update_production'),

]
