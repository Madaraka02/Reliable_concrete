from django.forms import ModelForm
from .models import *
from django import forms
from datetime import date


today = date.today()
class DatePickerInput(forms.DateInput):
    input_type = 'date'


class MaterialForm(ModelForm):
    class Meta:
        model = RawMaterial
        # fields = '__all__'
        exclude = ('available_qty',)
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        }    


class MaterialUseForm(ModelForm):
    class Meta:
        model = RawMaterialUsage
        fields = '__all__'
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        } 
