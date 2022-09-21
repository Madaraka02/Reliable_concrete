from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from materials.models import *
from stocks.models import *
from stocks.forms import *
from sales.forms import *
# from datetime import datetime
from django.contrib import messages
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
        'curring':curring,
        'current_date':current_date

    }
    return render(request, 'curing.html', context)


def production_report(request):
    curring = CuringStock.objects.all()
    productions = Production.objects.all().order_by('-id')   
    productionss = Moulding.objects.all() 
    mouldimgs = Moulding.objects.all()   
    context = {
        'productions':productions,
        'productionss':productionss,
        'curring':curring,
        'mouldimgs':mouldimgs
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
    productio = get_object_or_404(Moulding, id=id)
    # stock_to_transfer = Moulding.objects.filter(product=productio, damages_confirmed=True)
    # transfered = produced - stocks_to_transfer

    current_date = datetime.today()
    if productio.transfered_to_curing == False:

        curing_stock = CuringStock.objects.create(product=productio,enter_date=current_date,transfered_to_ready=False)
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
        # ready_stock.save()
        productio.transfered_to_ready = True
        # productio.save()

 
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

    ready_for_sale = ReadyForSaleStock.objects.order_by('stock__product').distinct()     
    context = {
        'ready_for_sale':ready_for_sale
    }
    return render(request, 'ready.html', context)


def sale_stock(request, id):
    ready = get_object_or_404(ReadyForSaleStock, id=id)
    avail_qty = ready.stock.product.qty_to_be_produced - ready.quantity_sold
    curr_in_db = ready.quantity_sold
    # 50-10= 40 SaleStockForm
    form = SaleStockForm(instance=ready)
    if request.method == 'POST':
        form = SaleStockForm(request.POST,request.FILES, instance=ready)
        if form.is_valid():
            user_qty = int(form.data['quantity'])
            # 10
            if user_qty > avail_qty:
                messages.warning(request, f'Your have only {avail_qty} units to sale {user_qty} is too much')
                return redirect('ready_stock_report')

            sale = form.save(commit=False)
            print(sale.quantity)
            print(sale.amount)
            print(sale.order_type)

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


            sale.product.quantity_sold=new_qty
            sale.product.selling = True 
            sale.product.sold = True    
            sale.product.date_sold = current_date
            sale.save()

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

        if mname == 'River_sand':
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

def moulding(request):
    # product = get_object_or_404(Product, id=id)
    materials = RawMaterial.objects.all()
    form = MouldingForm()
    if request.method == 'POST':
        form = MouldingForm(request.POST)
        if form.is_valid():
            user_prd = form.data['product']
            user_qty = form.data['qty_to_be_produced']

            product = get_object_or_404(ProductMaterialConsumption, id=user_prd)
            estimated_oil = product.oil * int(user_qty)
            estimated_diesel = product.diesel * int(user_qty)
            estimated_cement = product.cement * int(user_qty)
            estimated_white_cement = product.white_cement * int(user_qty)
            estimated_sand = product.sand * int(user_qty)
            estimated_river_sand = product.river_sand * int(user_qty)
            estimated_quarter_ballast = product.quarter_ballast * int(user_qty)
            estimated_half_ballast = product.half_ballast * int(user_qty)
            estimated_pumice = product.pumice * int(user_qty)
            estimated_dust = product.dust * int(user_qty)
            print(estimated_oil)
            




            for material in materials:
                mname = material.name
                mqty = material.available_qty

                if mname == 'Sand':
                    if mqty < estimated_sand:
                        messages.warning(request, f"No enough sand")
                        return redirect('production_report')

                if mname == 'Half_ballast':
                    if mqty < estimated_half_ballast:
                        messages.warning(request, f"No enough Half ballast")
                        return redirect('production_report')
                
                if mname == 'Oil':
                    if mqty < estimated_oil:
                        messages.warning(request, f"No enough Oil")
                        return redirect('production_report')

                if mname == 'Diesel':
                    if mqty < estimated_diesel:
                        messages.warning(request, f"No enough Diesel")
                        return redirect('production_report')

                if mname == 'Cement':
                    if mqty < estimated_cement:
                        messages.warning(request, f"No enough Cement")
                        return redirect('production_report')  
                
                if mname == 'White_cement':
                    if mqty < estimated_white_cement:
                        messages.warning(request, f"No enough White Cement")
                        return redirect('production_report')  


                if mname == 'Quarter_ballast':
                    if mqty < estimated_quarter_ballast:
                        messages.warning(request, f"No enough Quarter Ballast")
                        return redirect('production_report') 

                if mname == 'Dust':
                    if mqty < estimated_dust:
                        messages.warning(request, f"No enough Dust")
                        return redirect('production_report')

                if mname == 'Pumice':
                    if mqty < estimated_pumice:
                        messages.warning(request, f"No enough Pumice")
                        return redirect('production_report')

                if mname == 'River_sand':
                    if mqty < estimated_river_sand:
                        messages.warning(request, f"No enough River Sand")
                        return redirect('production_report')

                    form.save()
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
            return redirect('production_report')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from datetime import datetime




def materials_receipt(request, id):
    # Create a file-like buffer to receive PDF data.
    
    production = get_object_or_404(Moulding, id=id)
    target_product = production.product
    client = get_object_or_404(ReleaseQty, product=target_product)
    prd_name = client.product.product.name
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
    p.drawString(500,720, f"Date: {client.date.strftime('%Y-%m-%d')}")


    # date_time = now.



    # Close the PDF object cleanly, and we're done.
    # p.showPage()

    # p.setPageSize((500, 300))
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Receipt.pdf') 



def production_damage(request):
    form = ProductionDamageForm()
    if request.method == 'POST':
        form = ProductionDamageForm(request.POST)
        if form.is_valid():
            proddamage = form.save(commit=False)
            proddamage.category = "PRODUCTION"
            proddamage.save()

            return redirect('production_report')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 

def curing_damage(request):
    product = get_object_or_404(CuringStock, id=id)
    form = curingDamageForm(instance=product)
    if request.method == 'POST':
        form = curingDamageForm(request.POST,instance=product)
        if form.is_valid():
            proddamage = form.save(commit=False)
            proddamage.product = product
            proddamage.category = "CURING"
            proddamage.save()

            return redirect('curing_report')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 


def packing_damage(request):
    form = PackingDamageForm()
    if request.method == 'POST':
        form = PackingDamageForm(request.POST)
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
        form = TransitDamageForm(request.POST)
        if form.is_valid():
            proddamage = form.save(commit=False)
            proddamage.category = "TRANSIT"
            proddamage.save()
            messages.success(request, f"Damages recorded")
            return redirect('transit_damage')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)     

def offloading_damage(request):
    form = OffloadingDamageForm()
    if request.method == 'POST':
        form = OffloadingDamageForm(request.POST)
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