from django.urls import path
from .views import *
from production.views import *

urlpatterns = [
    path('', stock, name='stock'),
    path('stock/take', stock_take, name='stock_take'),
    path('count/', stocks_count, name='stocks_count'),
    path('report/', stock_report, name='stock_report'),
    path('export/csv/', export_users_xls, name='export_users_csv'),
]