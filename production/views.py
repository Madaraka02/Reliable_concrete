from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.

def production(request):
    form = ProductionForm()
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('production')
    context = {
        'form':form
    }        
    return render(request, 'form.html',context)    

def production_report(request):
    productions = Production.objects.all()       
    context = {
        'productions':productions
    }
    return render(request, 'production_report.html', context)
