from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('damages', damages_report, name='damages_report')

]