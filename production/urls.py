from django.urls import path
from .views import *



urlpatterns = [
    path('', production_post, name='production'),
    path('add-product/', add_product, name='add_product'),
    path('product/material/consumption/', prod_consumption_report, name='prod_consumption_report'),
    path('<int:id>/product/material/consumption/', update_product_material_consmption, name='update_product_material_consmption'),

    path('add-product/material/consumption/', add_product_material_consmption, name='add_product_material_consmption'),

    
    path('stocks/search/', search_count, name='search_count'),

    path('products/', products_report, name='products_report'),
    path('report/', production_report, name='production_report'),
    path('curing/report/', curing_report, name='curing_report'),
    path('ready/report/', ready_stock_report, name='ready_stock_report'),
    path('production/export/excel/', export_production_xls, name='export_production_xls'),
    path('products/export/excel/', export_products_xls, name='export_products_xls'),
    path('products/<int:id>/update/', edit_product, name='update_product'),
    path('<int:id>/update/', update_production, name='update_production'),
    path('<int:id>/delete/', delete_product, name='delete_product'),
    path('<int:id>/transfer-to-curnig/', transfer_to_curnig, name='transfer_to_curnig'),
    path('<int:id>/transfer-to-ready/', transfer_stock_to_ready, name='transfer_stock_to_ready'),
    path('<int:id>/sale/', sale_stock, name='sale_stock'),
    path('plan/', add_production_target, name='add_production_target'),
    path('moulding/', moulding, name='moulding'),
    path('moulding/<str:id>/update/', update_product, name='update_product'),

    path('transfer-ready/', transfer_to_ready, name='transfer_to_ready'),
    path('<int:id>/damage/', production_damage, name='production_damage'),
    path('<int:id>/curing/damage/', curing_damage, name='curing_damage'),
    path('packing/damage/', packing_damage, name='packing_damage'),
    path('transit/damage/', transit_damage, name='transit_damage'),
    path('offloading/damage/', offloading_damage, name='offloading_damage'),
    path('<int:id>/material-receipt/', materials_receipt, name='materials_receipt'),

    path('<int:id>/semi-material-receipt/', semi_materials_receipt, name='semi_materials_receipt'),

    path('<int:id>/material/consumption/', material_product_rship, name='material_product_rship'),

]

