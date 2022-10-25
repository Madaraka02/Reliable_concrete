from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from materials.forms import *

import csv
import xlwt
from django.http import HttpResponse

def export_stocks_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stocks.csv"'

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


def dispatch_stock_to_branch(request):
    form = DispatchStockToBranchForm()
    if request.method == 'POST':
        form = DispatchStockToBranchForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])
            product = form.data['product']
            to_branch = form.data['to']

            stock_dispatch = form.save()


            prod = get_object_or_404(ReadyForSaleStock,id=product)
    
            count_qty=prod.remaining_stock
            already_sold=prod.quantity_sold
            updated_qty=0
            if count_qty > qty:
                updated_qty=already_sold+qty
                
            else:
                # raise production notification
                return redirect('home')    
                
            prod.quantity_sold=updated_qty
            prod.save()

            branch = get_object_or_404(Branch, id=to_branch) #get branch

            branchh_material = BranchStockCounts.objects.get(product=prod, branch=to_branch) #get branch material to get available material
             #get branch material to get available material

            qqty=branchh_material.quantity
            upqty=qqty+qty
            branchh_material.quantity=upqty

            branchh_material.save()

            return redirect('dispatch_stock_to_branch')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  


def dispatch_stock_to_site(request):
    form = DispatchStockToSiteForm()
    if request.method == 'POST':
        form = DispatchStockToSiteForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])
            product = form.data['product']
            to_branch = form.data['to']

            stock_dispatch = form.save()


            prod = get_object_or_404(ReadyForSaleStock,id=product)
    
            count_qty=prod.remaining_stock
            already_sold=prod.quantity_sold
            updated_qty=0
            if count_qty > qty:
                updated_qty=already_sold+qty
            else:
                return redirect('home')    
                
            prod.quantity_sold=updated_qty
            prod.save()

            site = get_object_or_404(Site, id=to_branch) #get site

            branchh_material = SiteStockCounts.objects.get(product=prod, site=to_branch) #get branch material to get available material
             #get branch material to get available material

            qqty=branchh_material.quantity
            upqty=qqty+qty
            branchh_material.quantity=upqty

            branchh_material.save()

            return redirect('dispatch_stock_to_site')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 


def branch_stock_sale(request, id):
    branch = get_object_or_404(Branch,id=id)

    form = BranchStockSaleForm()
    if request.method == 'POST':
        form = BranchStockSaleForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])
            amt = int(form.data['amount'])

            product=form.data['product']
            prod = get_object_or_404(ReadyForSaleStock,id=product)
            # materiall = get_object_or_404(MaterialCounts,material=materia)
            branch_material = BranchStockCounts.objects.get(branch=branch, product=prod) #get branch material to get available material

            avail_qty =branch_material.quantity
            if avail_qty > qty:

                branch_material_sale = form.save()
            else:
                # create request to main site for additional materials
                return redirect('home')    
            

            qqty=branch_material.quantity
            upqty=avail_qty-qty
            branch_material.quantity=upqty

            # print(branch.name)
            branch_material.save()

            sale_timestamp = SalesTimestamp.objects.create(
                sale=prod,quantity_sold=qty,amount_sold=amt,sale_branch=branch,date_sold=current_date)
            sale_timestamp.save()
            return redirect('branch_stock_sale',id=id)
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  