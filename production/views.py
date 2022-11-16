from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from materials.models import *
from materials.forms import *
from stocks.models import *
from stocks.forms import *
from sales.forms import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from datetime import datetime, date, timedelta
from .utils import *
from django.db.models import Q

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

def search_count(request):
    query = request.GET.get("q")
    search_res = StockCounts.objects.filter(product__product__name__icontains=query)

    context = {
        'search_res':search_res,
    }
    return render(request, 'availablestocks.html', context)


def stocks_count(request):  
    # paginate curing report table
    stocks_list = StockCounts.objects.all().order_by('-id')
    # x= [x.product.product.product.name for x in curring_list]
    # y= [x.quantity_transfered for x in curring_list]
    # chart = get_plot(x, y)
    page = request.GET.get('page', 1)

    paginator = Paginator(stocks_list, 15)
    try:
        available_stocks = paginator.page(page)
    except PageNotAnInteger:
        available_stocks = paginator.page(1)
    except EmptyPage:
        available_stocks = paginator.page(paginator.num_pages) 

    context = {
        'available_stocks':available_stocks,
        'current_date':current_date,
        # 'chart':chart

    }
    return render(request, 'availablestocks.html', context)

def curing_report(request):  
    # paginate curing report table
    curring_list = CuringStock.objects.all().order_by('-id')
    # x= [x.product.product.product.name for x in curring_list]
    # y= [x.quantity_transfered for x in curring_list]
    # chart = get_plot(x, y)
    page = request.GET.get('page', 1)

    paginator = Paginator(curring_list, 9)
    try:
        curring = paginator.page(page)
    except PageNotAnInteger:
        curring = paginator.page(1)
    except EmptyPage:
        curring = paginator.page(paginator.num_pages) 

    context = {
        'curring':curring,
        'current_date':current_date,
        # 'chart':chart

    }
    return render(request, 'curing.html', context)


def production_report(request):
    curring = CuringStock.objects.all()
    productions = Production.objects.all().order_by('-id')   
    productionss = Moulding.objects.all().order_by('-id')


    # paginate production report table
    mouldimgs_list = Moulding.objects.all().order_by('-id')
    x= [x.product.product.name for x in mouldimgs_list]
    y= [y.qty_to_be_produced for y in mouldimgs_list]
    chart = get_prod_plot(x, y)  
    page = request.GET.get('page', 1)

    paginator = Paginator(mouldimgs_list, 9)
    try:
        mouldimgs = paginator.page(page)
    except PageNotAnInteger:
        mouldimgs = paginator.page(1)
    except EmptyPage:
        mouldimgs = paginator.page(paginator.num_pages)  

    context = {
        'productions':productions,
        'productionss':productionss,
        'curring':curring,
        'mouldimgs':mouldimgs,
        'chart':chart
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
            messages.success(request, 'Updated successfully')

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




def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            messages.success(request, 'Product updated successfully.')

            return redirect('products_report')
    context = {
        'form':form,
        'product':product
        
    }        
    return render(request, 'form.html',context)      

def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Product added successfully. Add product material consumption')

            return redirect('add_product_material_consmption')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  
    #  productions = Production.objects.filter(date__month='9')  

def add_product_material_consmption(request):
    form = ProductMaterialConsumptionForm()
    if request.method == 'POST':
        form = ProductMaterialConsumptionForm(request.POST)
        if form.is_valid():
            pp = form.save(commit=False)
            pp.save()

            stcok = StockCounts.objects.create(product=pp,quantity=0,date=current_date)
            stcok.save()
            
            messages.success(request, 'Material consumption added successfully and more products')
            

            return redirect('add_product')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 


def prod_consumption_report(request):
    # paginate product material consumption report table
    prod_cons_list = ProductMaterialConsumption.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(prod_cons_list, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)  

    context = {
        'products':products
    }
    return render(request, 'product_consumption.html', context)   


def update_product_material_consmption(request, id):
    product = get_object_or_404(ProductMaterialConsumption, id=id)
    form = ProductMaterialConsumptionForm(instance=product)
    if request.method == 'POST':
        form = ProductMaterialConsumptionForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully')

            return redirect('prod_consumption_report')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 

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
    materials = RawMaterial.objects.all()
    product = get_object_or_404(Moulding, id=id)
    form = MouldingUpdateForm(instance=product)
    if request.method == 'POST':
        form = MouldingUpdateForm(request.POST, instance=product)
        if form.is_valid():
            user_qty = int(float(form.data['qty_to_be_produced']))
            pp = form.save(commit=False)
            
            pp.production_ended = True
            pp.save()


            prod = product.product
            estimated_oil = prod.oil * int(user_qty)
            estimated_diesel = prod.diesel * int(user_qty)
            estimated_cement = prod.cement * int(user_qty)
            estimated_white_cement = prod.white_cement * int(user_qty)
            estimated_sand = prod.sand * int(user_qty)
            estimated_river_sand = prod.river_sand * int(user_qty)
            estimated_quarter_ballast = prod.quarter_ballast * int(user_qty)
            estimated_half_ballast = prod.half_ballast * int(user_qty)
            estimated_pumice = prod.pumice * int(user_qty)
            estimated_dust = prod.dust * int(user_qty)
            print(estimated_oil)
            




            material_receipt = ReleaseQty.objects.create(
            product =product,
            oil=estimated_oil,
            diesel=estimated_diesel,
            cement=estimated_cement,
            white_cement=estimated_white_cement,
            sand=estimated_sand,
            river_sand=estimated_river_sand,
            quarter_ballast=estimated_quarter_ballast,
            half_ballast=estimated_half_ballast,
            pumice=estimated_pumice,
            dust=estimated_dust,
            date=current_date
            )
            material_receipt.save()
            messages.success(request, 'Updated successfully')

            return redirect('production_report')
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
    productio = get_object_or_404(Moulding, id=id)
    # stock_to_transfer = Moulding.objects.filter(product=productio, damages_confirmed=True)
    # transfered = produced - stocks_to_transfer
    available_qty = productio.qty_to_be_produced
    name = productio.product.product.name
    # damaged =get_object_or_404(Damage, product=productio)
    damaged = Damage.objects.filter(product=productio).filter(category='PRODUCTION')
    qty_dam = 0
    for d in damaged:
        qty_dam = d.quantity_damaged
    # print(damaged)
    
    # print(qty_dam)

    qty_good = available_qty - qty_dam

    current_date = datetime.today()
    if productio.transfered_to_curing == False and productio.damgess < available_qty:

        curing_stock = CuringStock.objects.create(product=productio,enter_date=current_date,transfered_to_ready=False)
        take_count = get_object_or_404(StockCounts, product__product__name = name)
        take_count.quantity += qty_good
        take_count.date = current_date
        take_count.save()
        
        # for take_count in take_counts:
        #     print(take_count.quantity)
        #     if take_count.product.product.name == name:
        #         take_count.quantity += qty_good
        #         # take_count.save()

        #         print('yes')


               
        # productio.qty_to_be_produced = qty_good
        productio.transfered_to_curing = True
        productio.save()
        curing_stock.save()
        messages.success(request, 'Transfered to curing')
        return redirect('production_report')


 
    # for stock in stocks_to_transfer:
    #     # date_1 = datetime.strptime(stock.date, '%m-%d-%Y')
    #     date_2 = stock.date + timedelta(days=1)
    #     if current_date == date_2:
    #         stock.transfered_to_curing = True
    #         print(stock)
    #         CuringStock.objects.create(product=stock,enter_date=current_date,curing_days=3,transfered_to_ready=False)
    #         CuringStock.save()
    messages.success(request, 'Nothing to transfer all products were damaged')

    return redirect('production_report')
            
def transfer_to_ready(request):
    stock_to_transfer = CuringStock.objects.filter(transfered_to_ready=False)

    print(stock_to_transfer)
    current_date = datetime.today()

    for stock in stocks_to_transfer:
        enterdate = stock.enter_date
        days_cure = stock.product.product.curing_days
        date_enter = enterdate.date()
        date_out = date_enter + timedelta(days=days_cure)

        if current_date == date_out:
            ready_stock = ReadyForSaleStock.objects.create(stock=stock, sold=False, date_received=current_date, quantity_sold=0)
            ready_stock.save()

            stock.transfered_to_ready = True
            stock.save()

    return redirect('curing_report')            
    

def transfer_stock_to_ready(request,id):
    productio = get_object_or_404(CuringStock, id=id)
    # stock_to_transfer = CuringStock.objects.filter(transfered_to_curing=False)
    # transfered = produced - stocks_to_transfer
    current_date = datetime.today()
    if productio.transfered_to_ready == False:
        enterdate = productio.enter_date
        days_cure = productio.product.product.curing_days
        
        date_enter = enterdate.date()
        date_out = date_enter + timedelta(days=days_cure)
      
       

        ready_stock = ReadyForSaleStock.objects.create(stock=productio, sold=False, date_received=current_date, quantity_sold=0)
        ready_stock.save()
        productio.transfered_to_ready = True
       
        productio.save()
        messages.success(request, 'transfered to ready')

 
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
    # .filter(stuff).values("ip_address").distinct().count()
    # Visit.objects.filter(stuff).values("ip_address").annotate(n=models.Count("pk"))

    # id_list = Log.objects.order_by('-date').values_list('project_id').distinct()[:4]
    # entries = Log.objects.filter(id__in=id_list)

    # image_list = Image.objects.order_by('collection__id').distinct('collection__id')

      
    ready_list = ReadyForSaleStock.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(ready_list, 15)
    try:
        ready_for_sale = paginator.page(page)
    except PageNotAnInteger:
        ready_for_sale = paginator.page(1)
    except EmptyPage:
        ready_for_sale = paginator.page(paginator.num_pages)   
    context = {
        'ready_for_sale':ready_for_sale
    }
    return render(request, 'ready.html', context)


def sale_stock(request, id):
    ready = get_object_or_404(ReadyForSaleStock, id=id)
    avail_qty = ready.stock.quantity_transfered - ready.quantity_sold
    curr_in_db = ready.quantity_sold
    name = ready.stock.product.product.product.name
    main='R.C.W'
    # 50-10= 40 SaleStockForm
    form = SaleStockForm(instance=ready)
    if request.method == 'POST':
        form = SaleStockForm(request.POST,request.FILES, instance=ready)
        if form.is_valid():
            user_qty = int(form.data['quantity'])
            sale_amt = int(form.data['amount'])

            # 10
            if user_qty > avail_qty:
                messages.warning(request, f'Your have only {avail_qty} units to sale {user_qty} is too much')
                return redirect('ready_stock_report')

            sale = form.save(commit=False)
            sale.product = ready
            new_qty = user_qty + curr_in_db
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
                sale.product.quantity_sold=new_qty
                print(f'send to db {sale.product.quantity_sold}')

            sale.product.quantity_sold=new_qty  #updates readystock model to this ne value
            sale.product.selling = True   #updates readystock model to this ne value
            sale.product.sold = True     #updates readystock model to this ne value 
            sale.product.date_sold = current_date  #updates readystock model to this ne value
            sale_snap = SalesTimestamp.objects.create(sale=ready,quantity_sold=user_qty,amount_sold=sale_amt,sale_branch=main,date_sold=current_date)
            sale_snap.save() #takes a spanshot of the sale
            sale.save()
            
            
            take_count = get_object_or_404(StockCounts, product__product__name = name)
            avail_count = take_count.quantity
            take_count.date =current_date
            take_count.quantity -= user_qty
            take_count.save()

            return redirect('ready_stock_report')
    context = {
        'form':form,
        'ready':ready
        
    }        
    return render(request, 'form.html',context) 


def material_product_rship(request, id):
    productconsumption = get_object_or_404(Moulding, id=id)
    materials = RawMaterial.objects.all()

    # productions = ProductMaterialConsumption.objects.all()




    hballast = productconsumption.half_ballast_kgs
    sand = productconsumption.sand_kgs
    oil = productconsumption.oil_ltrs
    diesel = productconsumption.diesel_ltrs
    cement = productconsumption.cement_kgs
    wcement = productconsumption.white_cement_kgs
    rsand = productconsumption.rsand_kgs
    qballast = productconsumption.quarter_ballast_kgs
    dust = productconsumption.dust_kgs
    pumice = productconsumption.pumice_kgs
    d8=productconsumption.d8_length
    
    for material in materials:
        
        # print(productconsumption)
        mname = material.name
        mqty = material.quantity
        print(f'psand {sand}')
        # print(f'phballast {phballast}')
        # print(mname)
        # print(mqty)
        # sandstock = 0



        if mname == 'Sand':
            remainder = mqty - sand
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=sand, date=current_date)
            rm.save()

        if mname == 'D8':
            remainder = mqty - d8
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=d8, date=current_date)
            rm.save()

        if mname == 'Half_ballast':
            # hballaststock = material.quantity
            remainder = mqty - hballast
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=hballast, date=current_date)
            rm.save()
        
        if mname == 'Oil':
            remainder = mqty - oil
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=oil, date=current_date)
            rm.save()

        if mname == 'Diesel':
            remainder = mqty - diesel
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=diesel, date=current_date)
            rm.save()

        if mname == 'Cement':
            remainder = mqty - cement
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=cement, date=current_date)
            rm.save()     
        
        if mname == 'White_cement':
            remainder = mqty - wcement
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=wcement, date=current_date)
            rm.save() 


        if mname == 'Quarter_ballast':
            remainder = mqty - qballast
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=qballast, date=current_date)
            rm.save() 

        if mname == 'Dust':
            remainder = mqty - dust
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=dust, date=current_date)
            rm.save()

        if mname == 'Pumice':
            remainder = mqty - pumice
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=pumice, date=current_date)
            rm.save()    

        if mname == '    ':
            remainder = mqty - rsand
            material.available_qty = remainder
            material.save()
            rm = RawMaterialUsage.objects.create(material=material,
            product=productconsumption.product,quantity=rsand, date=current_date)
            rm.save()

    productconsumption.production_confirmed=True
    productconsumption.save()
    return redirect('production_report')

    # context = {
    #     'material':material,
    #     'productconsumption':productconsumption,
        


    # }
    # return render(request, 'production_report.html', context)    
import decimal
def moulding(request):
    # product = get_object_or_404(Product, id=id)
    productions = Moulding.objects.filter(date=current_date)


    materials = RawMaterial.objects.all()
    form = MouldingForm()
    if request.method == 'POST':
        form = MouldingForm(request.POST)
        if form.is_valid():
            user_prd = form.data['product']
            user_qty = int(float(form.data['qty_to_be_produced']))

            target_product=get_object_or_404(ProductMaterialConsumption, id=user_prd)
            for prodd in productions:
                
                if prodd.product == target_product:
                    moulded=get_object_or_404(Moulding, product=target_product)
                    messages.warning(request, f"This product is already being produced update quantity instead")
                    return redirect('update_product', id=moulded.id)
                    
                else:
                    print('no')    

            product = get_object_or_404(ProductMaterialConsumption, id=user_prd)
            estimated_oil = product.oil * decimal.Decimal(user_qty)
            estimated_diesel = product.diesel * decimal.Decimal(user_qty)
            estimated_cement = product.cement * decimal.Decimal(user_qty)
            estimated_white_cement = product.white_cement * decimal.Decimal(user_qty)
            estimated_sand = product.sand * decimal.Decimal(user_qty)
            estimated_river_sand = product.river_sand * decimal.Decimal(user_qty)
            estimated_quarter_ballast = product.quarter_ballast * decimal.Decimal(user_qty)
            estimated_half_ballast = product.half_ballast * decimal.Decimal(user_qty)
            estimated_pumice = product.pumice * decimal.Decimal(user_qty)
            estimated_dust = product.dust * decimal.Decimal(user_qty)
            estimated_d8 = product.D8 * decimal.Decimal(user_qty)

            print(estimated_cement)
            




            for material in materials:
                mname = material.name
                mqty = material.available_qty

                if mname == 'Sand':
                    if mqty < estimated_sand:
                        messages.warning(request, f"No enough sand")
                        return redirect('production_report')

                elif mname == 'Half_ballast':
                    if mqty < estimated_half_ballast:
                        messages.warning(request, f"No enough Half ballast")
                        return redirect('production_report')
                

                elif mname == 'D8':
                    if mqty < estimated_d8:
                        messages.warning(request, f"No enough D8")
                        return redirect('production_report')

                elif mname == 'Oil':
                    if mqty < estimated_oil:
                        messages.warning(request, f"No enough Oil")
                        return redirect('production_report')

                elif mname == 'Diesel':
                    if mqty < estimated_diesel:
                        messages.warning(request, f"No enough Diesel")
                        return redirect('production_report')

                elif mname == 'Cement':
                    if mqty < estimated_cement:
                        messages.warning(request, f"No enough Cement")
                        return redirect('production_report')  
                
                elif mname == 'White_cement':
                    if mqty < estimated_white_cement:
                        messages.warning(request, f"No enough White Cement")
                        return redirect('production_report')  


                elif mname == 'Quarter_ballast':
                    if mqty < estimated_quarter_ballast:
                        messages.warning(request, f"No enough Quarter Ballast")
                        return redirect('production_report') 

                elif mname == 'Dust':
                    if mqty < estimated_dust:
                        messages.warning(request, f"No enough Dust")
                        return redirect('production_report')

                elif mname == 'Pumice':
                    if mqty < estimated_pumice:
                        messages.warning(request, f"No enough Pumice")
                        return redirect('production_report')

                elif mname == 'River_sand':
                    if mqty < estimated_river_sand:
                        messages.warning(request, f"No enough River Sand")
                        return redirect('production_report')

                mould = form.save()

            semi_material_receipt = SemiReleaseQty.objects.create(
            product =mould,
            oil=estimated_oil,
            diesel=estimated_diesel,
            cement=estimated_cement,
            white_cement=estimated_white_cement,
            sand=estimated_sand,
            river_sand=estimated_river_sand,
            quarter_ballast=estimated_quarter_ballast,
            half_ballast=estimated_half_ballast,
            pumice=estimated_pumice,
            dust=estimated_dust,
            D8=estimated_d8,
            date=current_date
            )
            semi_material_receipt.save()    


            # material_receipt = ReleaseQty.objects.create(
            # product =product,
            # oil=estimated_oil,
            # diesel=estimated_diesel,
            # cement=estimated_cement,
            # white_cement=estimated_white_cement,
            # sand=estimated_sand,
            # river_sand=estimated_river_sand,
            # quarter_ballast=estimated_quarter_ballast,
            # half_ballast=estimated_half_ballast,
            # pumice=estimated_pumice,
            # dust=estimated_dust,
            # date=current_date
            # )
            # material_receipt.save()
            messages.success(request, 'Recorded successfully')

            return redirect('production_report')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from datetime import datetime

def semi_materials_receipt(request, id):
    # Create a file-like buffer to receive PDF data.
    
    production = get_object_or_404(Moulding, id=id)
    target_product = production.product
    client = get_object_or_404(SemiReleaseQty, product=production)
    # client = SemiReleaseQty.objects.filter(product=target_product)
    prd_name = client.product.product.product.name
    prd_namee = prd_name.upper()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 10)
    p.drawString(200,805, "RELIABLE CONCRETE WORKS PRODUCTION MATERIALS RECEIPT")
    p.drawString(200,790, f"FOR {prd_namee}")
    

    p.drawString(20,785, f"Receipt No: R{client.id}C{production.id}W{target_product.id}")

    # p.drawString(25,765, f"PRODUCT")
    p.drawString(50,765, f"OIL")
    p.drawString(100,765, f"DIESEL")
    p.drawString(150,765, f"CEMENT")
    p.drawString(200,765, f"W.CEMENT")
    p.drawString(260,765, f"SAND")
    p.drawString(300,765, f"R.SAND")
    p.drawString(350,765, f"1/4BALLAST")
    p.drawString(425,765, f"1/2BALLAST")
    p.drawString(500,765, f"PUMICE")
    p.drawString(550,765, f"DUST")
    p.drawString(575,765, f"D8")


    p.line(10,760,580,760)


  
    p.drawString(50,740, f"{client.oil}")
    p.drawString(100,740, f"{client.diesel}")
    p.drawString(150,740, f"{client.cement}")

    p.drawString(200,740, f"{client.white_cement}")
    p.drawString(260,740, f"{client.sand}")
    p.drawString(300,740, f"{client.river_sand}")
    p.drawString(350,740, f"{client.quarter_ballast}")
    p.drawString(425,740, f"{client.half_ballast}")
    p.drawString(500,740, f"{client.pumice}")
    p.drawString(550,740, f"{client.dust}")
    p.drawString(575,740, f"{client.D8}")

    p.drawString(500,720, f"Date: {client.date.strftime('%Y-%m-%d')}")


    # date_time = now.



    # Close the PDF object cleanly, and we're done.
    # p.showPage()

    # p.setPageSize((500, 300))
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='SemiReceipt.pdf') 



def materials_receipt(request, id):
    # Create a file-like buffer to receive PDF data.
    
    production = get_object_or_404(Moulding, id=id)
    target_product = production.product
    client = get_object_or_404(ReleaseQty, product=production)
    # client = ReleaseQty.objects.filter(product=target_product).first()
    prd_name = client.product.product.product.name
    prd_namee = prd_name.upper()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 10)
    p.drawString(200,805, "RELIABLE CONCRETE WORKS PRODUCTION MATERIALS RECEIPT")
    p.drawString(200,790, f"FOR {prd_namee}")
    

    p.drawString(20,785, f"Receipt No: R{client.id}C{production.id}W{target_product.id}")

    # p.drawString(25,765, f"PRODUCT")
    p.drawString(50,765, f"OIL")
    p.drawString(100,765, f"DIESEL")
    p.drawString(150,765, f"CEMENT")
    p.drawString(200,765, f"W.CEMENT")
    p.drawString(260,765, f"SAND")
    p.drawString(300,765, f"R.SAND")
    p.drawString(350,765, f"1/4BALLAST")
    p.drawString(425,765, f"1/2BALLAST")
    p.drawString(500,765, f"PUMICE")
    p.drawString(550,765, f"DUST")
    p.drawString(575,765, f"D8")


    p.line(10,760,580,760)


  
    p.drawString(50,740, f"{client.oil}")
    p.drawString(100,740, f"{client.diesel}")
    p.drawString(150,740, f"{client.cement}")

    p.drawString(200,740, f"{client.white_cement}")
    p.drawString(260,740, f"{client.sand}")
    p.drawString(300,740, f"{client.river_sand}")
    p.drawString(350,740, f"{client.quarter_ballast}")
    p.drawString(425,740, f"{client.half_ballast}")
    p.drawString(500,740, f"{client.pumice}")
    p.drawString(550,740, f"{client.dust}")
    p.drawString(575,740, f"{client.D8}")

    p.drawString(500,720, f"Date: {client.date.strftime('%Y-%m-%d')}")


    # date_time = now.



    # Close the PDF object cleanly, and we're done.
    # p.showPage()

    # p.setPageSize((500, 300))
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Receipt.pdf') 



def production_damage(request,id):
    product = get_object_or_404(Moulding, id=id)
    available_qty = product.qty_to_be_produced
    
    
    form = ProductionDamageForm()
    if request.method == 'POST':
        form = ProductionDamageForm(request.POST,request.FILES)
        if form.is_valid():
            dam = int(form.data['quantity_damaged'])
            proddamage = form.save(commit=False)
            transfered = available_qty-dam
            proddamage.product = product
            proddamage.category = "PRODUCTION"
            product.damgess = dam
            product.qty_transfered = transfered
            product.damages_confirmed = True
            proddamage.date = current_date
            product.save()

            proddamage.save()
            messages.success(request, 'Recorded  successfully')


            return redirect('transfer_to_curnig', id=id)
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 

def curing_damage(request,id):
    product = get_object_or_404(CuringStock, id=id)
    available_qty = product.product.qty_to_be_produced
    name = product.product.product.product.name


    form = curingDamageForm()
    if request.method == 'POST':
        form = curingDamageForm(request.POST,request.FILES)
        if form.is_valid():
            dam = int(form.data['quantity_damaged'])
            proddamage = form.save(commit=False)
            transfered = available_qty-dam
            proddamage.product = product.product
            proddamage.category = "CURING"
            proddamage.date = current_date
            product.damages_confirmed = True
            product.damaged = dam
            product.quantity_transfered = transfered
            product.save()
            proddamage.save()

            take_count = get_object_or_404(StockCounts, product__product__name = name)
            avail_count = take_count.quantity
            take_count.quantity -= dam
            take_count.date =current_date
            take_count.save()
            messages.success(request, 'Transfered successfully')

            return redirect('transfer_stock_to_ready', id=id)
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 


def packing_damage(request):
    form = PackingDamageForm()
    if request.method == 'POST':
        form = PackingDamageForm(request.POST,request.FILES)
        if form.is_valid():
            proddamage = form.save(commit=False)
            proddamage.category = "PACKING"
            proddamage.save()
            messages.success(request, f"Damages recorded")
            return redirect('packing_damage')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 

def transit_damage(request):
    form = TransitDamageForm()
    if request.method == 'POST':
        form = TransitDamageForm(request.POST,request.FILES)
        if form.is_valid():
            proddamage = form.save(commit=False)
            proddamage.category = "TRANSIT"
            proddamage.save()
            messages.success(request, f"Damages recorded at the office")
            return redirect('transit_damage')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)     

def offloading_damage(request):
    form = OffloadingDamageForm()
    if request.method == 'POST':
        form = OffloadingDamageForm(request.POST,request.FILES)
        if form.is_valid():
            proddamage = form.save(commit=False)
            proddamage.category = "OFFLOADING"
            proddamage.save()
            messages.success(request, f"Damages recorded")
            return redirect('offloading_damage')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)    



def stock_take(request):
    form = StockRecordingForm()
    if request.method == 'POST':
        form = StockRecordingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record saved successfully')
            return redirect('stock take')

    context = {
        'form':form,
        
    }
    return render(request, 'form.html', context)        






def create_site(request):
    materials = RawMaterial.objects.all()
    stocks = ReadyForSaleStock.objects.all()
    form = SiteForm()
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            site = form.save()
            # create material and stock counts with 0
             # site materials SiteMaterialCounts
            for material in materials:
                site_material = SiteMaterialCounts.objects.create(material=material, site=site,quantity=0,date=current_date)
                site_material.save()
           
            # site stocks  SiteStockCounts
            for stock in stocks:
                site_stock = SiteStockCounts.objects.create(site=site,product=stock,quantity=0, date=current_date)
                site_stock.save()
            messages.success(request, 'Site created successfully')


            return redirect('home')
    context = {
        'form':form,
    }        
    return render(request, 'form.html',context)   

def create_Branch(request):
    materials = RawMaterial.objects.all()
    stocks = ReadyForSaleStock.objects.all()

    form = BranchForm()
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save()
            # create material and stock counts with 0
            # branch materials BranchMaterialCounts
            for material in materials:
                branch_material = BranchMaterialCounts.objects.create(material=material, branch=branch,quantity=0,date=current_date)
                branch_material.save()
            # branch stocks  BranchStockCounts
            for stock in stocks:
                branch_stock = BranchStockCounts.objects.create(branch=branch,product=stock,quantity=0, date=current_date)
                branch_stock.save()
            
            
            messages.success(request, 'Branch created successfully')

            return redirect('home')
    context = {
        'form':form,
    }        
    return render(request, 'form.html',context)   
