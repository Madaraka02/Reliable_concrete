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

class ProductionDamageForm(ModelForm):
    class Meta:
        model = Damage
        fields = ['product','quantity_damaged','date', 'image']
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }


class curingDamageForm(ModelForm):
    class Meta:
        model = Damage
        fields = ['quantity_damaged','image']
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }

class PackingDamageForm(ModelForm):
    class Meta:
        model = Damage
        fields = ['product','quantity_damaged','date','image']
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }

class TransitDamageForm(ModelForm):
    class Meta:
        model = Damage
        fields = ['product','quantity_damaged','date','image']
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }

class OffloadingDamageForm(ModelForm):
    class Meta:
        model = Damage
        fields = ['product','quantity_damaged','date','image']
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }