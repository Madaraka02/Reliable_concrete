from django.urls import path
from .views import *


urlpatterns = [
    path('', production_post, name='production'),
    path('add-product/', add_product, name='add_product'),
    path('products/', products_report, name='products_report'),
    path('report/', production_report, name='production_report'),
    path('curing/report/', curing_report, name='curing_report'),
    path('ready/report/', ready_stock_report, name='ready_stock_report'),
    path('production/export/excel/', export_production_xls, name='export_production_xls'),
    path('products/export/excel/', export_products_xls, name='export_products_xls'),
    path('products/<int:id>/update/', update_product, name='update_product'),
    path('<int:id>/update/', update_production, name='update_production'),
    path('<int:id>/delete/', delete_product, name='delete_product'),
    path('<int:id>/transfer-to-curnig/', transfer_to_curnig, name='transfer_to_curnig'),
    path('<int:id>/transfer-to-ready/', transfer_stock_to_ready, name='transfer_stock_to_ready'),
    path('<int:id>/sale/', sale_stock, name='sale_stock'),
    path('plan/', add_production_target, name='add_production_target'),
    path('moulding/', moulding, name='moulding'),
    path('transfer-ready/', transfer_to_ready, name='transfer_to_ready'),


    path('<int:id>/material-receipt/', materials_receipt, name='materials_receipt'),
    path('<int:id>/material/consumption/', material_product_rship, name='material_product_rship'),

]
