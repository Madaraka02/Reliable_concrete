from django.shortcuts import render, redirect
from .models import *
from .forms import *

import csv
import xlwt


from django.http import HttpResponse

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Product', 'Ready', 'Curing', 'price per unit','Damages','Date'])

    stocks = Stock.objects.all().values_list('product', 'Ready', 'Curing', 'price_per_unit','damages','date')
    for stock in stocks:
        writer.writerow(stock)

    return response

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="stocks.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Stocks')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Ready', 'Curing', 'price per unit','Date',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Stock.objects.all().values_list('name', 'Ready', 'Curing', 'price_per_unit','date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
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
    stocks = Stock.objects.all()       
    context = {
        'stocks':stocks
    }
    return render(request, 'stock_report.html', context)    