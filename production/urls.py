from django.urls import path
from .views import *


urlpatterns = [
    path('', production_post, name='production'),
    path('add-product/', add_product, name='add_product'),
    path('products/', products_report, name='products_report'),
    path('report/', production_report, name='production_report'),
    path('production/export/excel/', export_production_xls, name='export_production_xls'),
    path('products/export/excel/', export_products_xls, name='export_products_xls'),
    path('products/<int:id>/update/', update_product, name='update_product'),
    path('<int:id>/update/', update_production, name='update_production'),
    path('<int:id>/delete/', delete_product, name='delete_product'),
]
