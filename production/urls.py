from django.urls import path
from .views import *

urlpatterns = [
    path('', production, name='production'),
    path('report/', production_report, name='production_report'),
]