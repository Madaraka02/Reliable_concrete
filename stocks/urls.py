from django.urls import path
from .views import *
from production.views import *

urlpatterns = [
    path('', stock, name='stock'),
    path('material/sales/', material_sales_report, name='material_sales_report'),

    path('create/site/',create_site, name='create_site'),
    path('create/branch/',create_Branch, name='create_Branch'),
    path('send/branch/',dispatch_stock_to_branch, name='dispatch_stock_to_branch'),
    path('send/site/',dispatch_stock_to_site, name='dispatch_stock_to_site'),
    path('branch/<str:id>/sale/', branch_stock_sale, name='branch_stock_sale'),
    path('site/<str:id>/use/', site_stock_use, name='site_stock_use'),

    path('home/',stock_home, name='stock_home'),
    path('store/home/',store_home, name='store_home'),
    path('site/home/',site_home, name='site_home'),
    path('branch/home/',branch_home, name='branch_home'),



    path('stock/take/', stock_take, name='stock_take'),
    path('count/', stocks_count, name='stocks_count'),
    path('report/', stock_report, name='stock_report'),
    path('export/csv/', export_users_xls, name='export_users_csv'),
]



# RasiseProductionNotification
