from django.forms import ModelForm
from .models import *
from django import forms
from datetime import date


today = date.today()
class DatePickerInput(forms.DateInput):
    input_type = 'date'

class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        widgets = {
            'date' : DatePickerInput(attrs={'max': today, 'min': today}),
        }