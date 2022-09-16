from django.forms import ModelForm
from .models import *
from django import forms
from datetime import date


today = date.today()
class DatePickerInput(forms.DateInput):
    input_type = 'date'


class SaleForm(ModelForm):
    class Meta:
        model = ReadyStock
        fields = ['sold','quantity_sold']
        # widgets = {
        #     'date' : DatePickerInput(attrs={'max': today}),
        # }
class ProductionTargetForm(ModelForm):
    class Meta:
        model = Production
        fields = ['product','target_production','date']
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }
class ProductionForm(ModelForm):
    class Meta:
        model = Production
        # fields = '__all__'
        exclude = ('transfered_to_curing',)
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
