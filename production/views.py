from django.shortcuts import render, redirect
from .models import *
from .forms import *

from datetime import datetime


month = datetime.now().month

# from datetime import date
# from dateutil.relativedelta import relativedelta

# from django.db.models.functions import Trunc

# six_months_ago = date.today() + relativedelta(months=-6)


# cases = Case.objects.all().filter(date_of_filling__month='1') 
# # Create your views here.

def production_post(request):
    form = ProductionForm()
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('production')
    context = {
        'form':form,
        'month':month
    }        
    return render(request, 'form.html',context)    

def production_report(request):
    productions = Production.objects.all()       
    context = {
        'productions':productions
    }
    return render(request, 'production_report.html', context)

def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('add_product')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  
    #  productions = Production.objects.filter(date__month='9')   

import xlwt


from django.http import HttpResponse


def export_production_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="production.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Stocks')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    






    columns = ['Product', 'Target', 'Actual', 'Damages', 'Date',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Production.objects.filter(date__month=month).values_list('product__name', 'target_production', 'actual_production', 'damages','date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response    