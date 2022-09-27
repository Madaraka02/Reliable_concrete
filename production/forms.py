from django.forms import ModelForm
from .models import *
from django import forms
from datetime import date


today = date.today()
class DatePickerInput(forms.DateInput):
    input_type = 'date'


class MouldingForm(ModelForm):
    class Meta:
        model = Moulding
        exclude = ('transfered_to_curing','production_confirmed','production_ended', 'damages_confirmed','qty_transfered','damgess')
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }

class MouldingUpdateForm(ModelForm):
    class Meta:
        model = Moulding
        fields = ['qty_to_be_produced',]
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }
        
class SaleForm(ModelForm):
    class Meta:
        model = ReadyStock
        fields = ['quantity_sold']
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

class ProductMaterialConsumptionForm(ModelForm):
    class Meta:
        model = ProductMaterialConsumption
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
