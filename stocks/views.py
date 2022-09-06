from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def stock(request):
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('stock')
    context = {
        'form':form
    }        
    return render(request, 'form.html',context)  

def stock_report(request):
    stocks = Production.objects.all()       
    context = {
        'stocks':stocks
    }
    return render(request, 'stock_report.html', context)    