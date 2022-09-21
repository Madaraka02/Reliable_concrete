from django.forms import ModelForm
from .models import *
from django import forms
from datetime import date


today = date.today()
class DatePickerInput(forms.DateInput):
    input_type = 'date'

class SaleStockForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['quantity','amount','order_type','order_documents']
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }