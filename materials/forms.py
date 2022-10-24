from django.forms import ModelForm
from .models import *
from stocks.models import *
from production.models import *
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



class BranchForm(ModelForm):
    class Meta:
        model=Branch
        fields = '__all__'

class SiteForm(ModelForm):
    class Meta:
        model=Site
        fields = '__all__'



class DispatchMaterialExternalForm(ModelForm):
    class Meta:
        model=DispatchMaterialExternal
        fields='__all__'
class DispatchMaterialToSiteForm(ModelForm):
    class Meta:
        model=DispatchMaterialToSite
        fields='__all__'



class DispatchStockToBranchForm(ModelForm):
    class Meta:
        model=DispatchStockToBranch
        fields='__all__'

class DispatchStockToSiteForm(ModelForm):
    class Meta:
        model=DispatchStockToSite
        fields='__all__'



class BranchMaterialSaleForm(ModelForm):
    class Meta:
        model=MaterialSale
        fields=['material','quantity']

class MainMaterialSaleForm(ModelForm):
    class Meta:
        model=MaterialSale
        fields=['quantity']
