from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

# from datetime import datetime
from datetime import datetime, date, timedelta

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

def curing_report(request):
    curring = CuringStock.objects.all().order_by('-id')      
    context = {
        'curring':curring
    }
    return render(request, 'curing.html', context)


def production_report(request):
    curring = CuringStock.objects.all()
    productions = Production.objects.all().order_by('-id')       
    context = {
        'productions':productions,
        'curring':curring
    }
    return render(request, 'production_report.html', context)

def products_report(request):
    products = Product.objects.all().order_by('-id')       
    context = {
        'products':products
    }
    return render(request, 'products.html', context)    

def update_production(request, id):
    production = get_object_or_404(Production, id=id)
    form = ProductionForm(instance=production)
    if request.method == 'POST':
        form = ProductionForm(request.POST, instance=production)
        if form.is_valid():
            form.save()

            return redirect('production_report')
    context = {
        'form':form,
        'production':production
        
    }        
    return render(request, 'form.html',context)  

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('products_report')

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

def add_production_target(request):
    form = ProductionTargetForm()
    if request.method == 'POST':
        form = ProductionTargetForm(request.POST)
        if form.is_valid():
            production_target = form.save(commit=False)
            production_target.actual_production = 0
            production_target.number_of_labourers = 0
            production_target.wage_per_labourer = 0
            production_target.oil_used_in_litres = 0
            production_target.fuel_used_in_litres = 0
            production_target.cement_bags_used = 0
            production_target.white_cement_bags_used = 0
            production_target.sand_buckets_used = 0
            production_target.river_sand_buckets_used = 0
            production_target.quarter_ballast_buckets_used = 0
            production_target.half_ballast_buckets_used = 0
            production_target.dust_buckets_used = 0
            production_target.damages = 0

            production_target.save()

            return redirect('production_report')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 


def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            return redirect('products_report')
    context = {
        'form':form,
        'product':product
        
    }        
    return render(request, 'form.html',context) 

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


def export_products_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Stocks')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Name', 'Description',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Product.objects.all().values_list('name', 'description',)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response        


def transfer_to_curnig(request,id):
    # produced = Production.objects.all().count()
    productio = get_object_or_404(Production, id=id)
    # stock_to_transfer = Production.objects.filter(productio=productio, transfered_to_curing=False)
    # transfered = produced - stocks_to_transfer
    current_date = datetime.today()
    if productio.transfered_to_curing == False:

        curing_stock = CuringStock.objects.create(product=productio,enter_date=current_date,curing_days=3,transfered_to_ready=False)
        curing_stock.save()
        productio.transfered_to_curing = True
        productio.save()

 
    # for stock in stocks_to_transfer:
    #     # date_1 = datetime.strptime(stock.date, '%m-%d-%Y')
    #     date_2 = stock.date + timedelta(days=1)
    #     if current_date == date_2:
    #         stock.transfered_to_curing = True
    #         print(stock)
    #         CuringStock.objects.create(product=stock,enter_date=current_date,curing_days=3,transfered_to_ready=False)
    #         CuringStock.save()

    return redirect('production_report')
            
    

def transfer_stock_to_ready(request,id):
    productio = get_object_or_404(CuringStock, id=id)
    # stock_to_transfer = Production.objects.filter(productio=productio, transfered_to_curing=False)
    # transfered = produced - stocks_to_transfer
    current_date = datetime.today()
    if productio.transfered_to_ready == False:

        ready_stock = ReadyStock.objects.create(stock=productio, sold=False, date_received=current_date, quantity_sold=0)
        ready_stock.save()
        productio.transfered_to_ready = True
        productio.save()

 
    # for stock in stocks_to_transfer:
    #     # date_1 = datetime.strptime(stock.date, '%m-%d-%Y')
    #     date_2 = stock.date + timedelta(days=1)
    #     if current_date == date_2:
    #         stock.transfered_to_curing = True
    #         print(stock)
    #         CuringStock.objects.create(product=stock,enter_date=current_date,curing_days=3,transfered_to_ready=False)
    #         CuringStock.save()

    return redirect('curing_report')    



def ready_stock_report(request):
    ready_for_sale = ReadyStock.objects.all().order_by('-id')      
    context = {
        'ready_for_sale':ready_for_sale
    }
    return render(request, 'ready.html', context)


def sale_stock(request, id):
    ready = get_object_or_404(ReadyStock, id=id)
    avail_qty = ready.stock.product.actual_production - ready.quantity_sold
    curr_in_db = ready.quantity_sold
    # 50-10= 40
    form = SaleForm(instance=ready)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=ready)
        if form.is_valid():
            user_qty = int(form.data['quantity_sold'])
            # 10
            if user_qty > avail_qty:
                return redirect('ready_stock_report')

            sale = form.save(commit=False)
            # new_qty = sale.quantity_sold + curr_in_db
            # print(f'Available for sale {avail_qty}') #30
            # print(f'current in db {curr_in_db}')#20
            # print(f'user {user_qty}')#10
            # print(f'form {sale.quantity_sold}')#10
            # print(f'updated {new_qty}')# 30
            # 10 + 10

            # if new_qty > avail_qty:
            #     print(f'Sorry thats to much you can only sale products less or equal {avail_qty}')
            #     return redirect('ready_stock_report')

            if new_qty < avail_qty:
                sale.quantity_sold=new_qty
                print(f'send to db {sale.quantity_sold}')


            sale.quantity_sold=new_qty
            sale.selling = True 
            sale.sold = True    
            sale.date_sold = current_date
            sale.save()

            return redirect('ready_stock_report')
    context = {
        'form':form,
        'ready':ready
        
    }        
    return render(request, 'form.html',context) 