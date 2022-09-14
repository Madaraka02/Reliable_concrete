from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

from datetime import datetime

# from datetime import date

# today = date.today()

# # dd/mm/YY
# d1 = today.strftime("%d/%m/%Y")


month = datetime.now().month
year = datetime.now().year

# Create your views here.

def material_report(request):
    materials = RawMaterial.objects.all()       
    context = {
        'materials':materials
    }
    return render(request, 'materials.html', context)

def update_material(request, id):
    material = get_object_or_404(RawMaterial, id=id)
    form = MaterialForm(instance=material)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()

            return redirect('material_report')
    context = {
        'form':form,
        'material':material
        
    }        
    return render(request, 'form.html',context)  


def add_material(request):
    form = MaterialForm()
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('add_material')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  
    #  productions = Production.objects.filter(date__month='9')   

import xlwt


from django.http import HttpResponse


def export_materials_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="materials.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Stocks')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    






    columns = ['Name', 'Quantity', 'Amount', 'Date',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = RawMaterial.objects.filter(date__month=month).values_list('name', 'quantity', 'amount', 'date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response    