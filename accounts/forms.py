
from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm
from .models import *



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'username', 'address', 'phone_number','is_production_staff', 'is_store_staff', 'is_sales_staff','is_branch_staff','is_site_staff','is_dispatch_staff','is_procurement_staff']

    

