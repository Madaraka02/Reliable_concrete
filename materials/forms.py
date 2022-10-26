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
        exclude = ('available_qty','confirm_received')
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

        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        } 

class DispatchMaterialToSiteForm(ModelForm):
    class Meta:
        model=DispatchMaterialToSite
        fields='__all__'

        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        } 




class DispatchStockToBranchForm(ModelForm):
    class Meta:
        model=DispatchStockToBranch
        fields='__all__'

        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        } 


class DispatchStockToSiteForm(ModelForm):
    class Meta:
        model=DispatchStockToSite
        fields='__all__'
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        } 



class BranchStockSaleForm(ModelForm):
    class Meta:
        model=BranchStockSale
        fields=['quantity', 'amount','date']

        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        } 
class BranchMaterialSaleForm(ModelForm):
    class Meta:
        model=MaterialSale
        fields=['quantity']

class MainMaterialSaleForm(ModelForm):
    class Meta:
        model=MaterialSale
        fields=['quantity']


class SiteMaterialUseForm(ModelForm):
    class Meta:
        model=SiteMaterialUse
        fields=['quantity', 'date']
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        } 


class SiteStockUseForm(ModelForm):
    class Meta:
        model=SiteStockUse
        fields=['quantity', 'date']
        widgets = {
            'date' : DatePickerInput(attrs={'max': today}),
        } 
 