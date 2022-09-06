from django.urls import path
from .views import *

urlpatterns = [
    path('', stock, name='stock'),
    path('report/', stock_report, name='stock_report'),
]