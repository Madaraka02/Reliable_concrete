from django.urls import path
from .views import *
from production.views import *

urlpatterns = [
    path('', stock, name='stock'),
    path('create/site',create_site, name='create_site'),
    path('create/branch',create_Branch, name='create_Branch'),
    path('stock/take', stock_take, name='stock_take'),
    path('count/', stocks_count, name='stocks_count'),
    path('report/', stock_report, name='stock_report'),
    path('export/csv/', export_users_xls, name='export_users_csv'),
]

# RasiseProductionNotification

# DispatchMaterialExternal
# DispatchMaterialToSite
# MaterialCounts
# BranchMaterialCounts
# SiteMaterialCounts
# TotalMaterialCounts
# BranchMaterialSale
# MaterialSale

# DispatchStockToSite
# SiteStockCounts
# DispatchStockToBranch
# BranchStockCounts
# BranchStockSale
