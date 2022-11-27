from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from production.models import *
from materials.models import *
from .forms import *
from materials.forms import *
from django.contrib.auth.decorators import login_required
import csv
import xlwt
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

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
            messages.success(request, 'Added successfully')

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
            name = prod.stock.product.product.product.name

    
            count_qty=prod.remaining_stock
            already_sold=prod.quantity_sold
            updated_qty=0
            if count_qty > qty:
                updated_qty=already_sold+qty
                
            else:
                # raise production notification
                return redirect('stock_home')    
                
            prod.quantity_sold=updated_qty
            prod.save()

            branch = get_object_or_404(Branch, id=to_branch) #get branch

            branchh_material = BranchStockCounts.objects.get(product=prod, branch=to_branch) #get branch material to get available material
             #get branch material to get available material

            qqty=branchh_material.quantity
            upqty=qqty+qty
            branchh_material.quantity=upqty

            branchh_material.save()

            available_stock = get_object_or_404(StockCounts,product__product__name = name)
            availl_count = available_stock.quantity
            available_stock.date =current_date
            available_stock.quantity -= qty
            available_stock.save()
            messages.success(request, 'Dispatched successfully')

            return redirect('stock_home')
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
            name = prod.stock.product.product.product.name
            count_qty=prod.remaining_stock
            already_sold=prod.quantity_sold
            updated_qty=0
            if count_qty > qty:
                updated_qty=already_sold+qty
            else:
                return redirect('stock_home')    
                
            prod.quantity_sold=updated_qty
            prod.save()

            site = get_object_or_404(Site, id=to_branch) #get site

            branchh_material = SiteStockCounts.objects.get(product=prod, site=to_branch) #get branch material to get available material
             #get branch material to get available material

            qqty=branchh_material.quantity
            upqty=qqty+qty
            branchh_material.quantity=upqty

            branchh_material.save()

            available_stock = get_object_or_404(StockCounts,product__product__name = name)
            availl_count = available_stock.quantity
            available_stock.date =current_date
            available_stock.quantity -= qty
            available_stock.save()
            messages.success(request, 'Dispatched successfully')

            return redirect('stock_home')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 


def branch_stock_sale(request, id):
    prod = get_object_or_404(ReadyForSaleStock,id=id)
    user=request.user
    branch=Branch.objects.get(manager=user)

    form = BranchStockSaleForm()
    if request.method == 'POST':
        form = BranchStockSaleForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])
            amt = int(form.data['amount'])

            # product=form.data['product']
            # prod = get_object_or_404(ReadyForSaleStock,id=product)
            
            # materiall = get_object_or_404(MaterialCounts,material=materia)
            branch_material = BranchStockCounts.objects.get(branch=branch, product=prod) #get branch material to get available material

            avail_qty =branch_material.quantity
            if avail_qty > qty:

                branch_material_sale = form.save(commit=False)
                branch_material_sale.branch=branch
                branch_material_sale.product=prod
                branch_material_sale.save()
            else:
                # create request to main site for additional materials
                return redirect('branch_home')    
            

            qqty=branch_material.quantity
            upqty=avail_qty-qty
            branch_material.quantity=upqty

            # print(branch.name)
            branch_material.save()

            sale_timestamp = SalesTimestamp.objects.create(
                sale=prod,quantity_sold=qty,amount_sold=amt,sale_branch=branch,date_sold=current_date)
            sale_timestamp.save()
            messages.success(request, 'Updated successfully')

            return redirect('branch_home')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  


def site_stock_use(request, id):
    product=get_object_or_404(ReadyForSaleStock, id=id)

    user=request.user
    site=Site.objects.get(manager=user)

    form = SiteStockUseForm()
    if request.method == 'POST':
        form = SiteStockUseForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])

            material_use = form.save(commit=False)
            material_use.site=site
            material_use.product=product
            material_use.save()

            material_count = SiteStockCounts.objects.get(product=product, site=site)
            count_qty=material_count.quantity
            updated_qty=0
            if count_qty > qty:
                updated_qty=count_qty-qty
            else:
                return redirect('home')    
                
            material_count.quantity=updated_qty
            material_count.save()
            messages.success(request, 'Updated successfully')

            return redirect('site_home')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)      


@login_required 
def stock_home(request):
    if request.user.is_staff or request.user.is_sales_staff:
        user=request.user

        stocks_list = StockCounts.objects.all().order_by('-id')
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

        }
            
        # StockCounts
        # DispatchStockToBranch
        # DispatchStockToSite
        return render(request, 'stock_home.html', context)
        

@login_required 
def store_home(request):
    if request.user.is_staff or request.user.is_store_staff:
        user=request.user

        raw_materials = Moulding.objects.all() 
        materials_list = RawMaterial.objects.all().order_by('-id')

        page = request.GET.get('page', 1)

        paginator = Paginator(materials_list, 5)
        try:
            materials = paginator.page(page)
        except PageNotAnInteger:
            materials = paginator.page(1)
        except EmptyPage:
            materials = paginator.page(paginator.num_pages) 
        context = {
            'materials':materials,
            'raw_materials':raw_materials,
        }
                # DispatchMaterialExternal
        # DispatchMaterialToSite
        # MaterialCounts
        # MaterialSale 
        return render(request, 'store_home.html', context)
    return redirect('home')    



@login_required 
def site_home(request):
    if request.user.is_staff or request.user.is_site_staff:
        user=request.user
        site=Site.objects.get(manager=user)

        materials_list = SiteMaterialCounts.objects.filter(site=site).order_by('-id')
        stock_list = SiteStockCounts.objects.filter(site=site).order_by('-id')

        page = request.GET.get('page', 1)

        paginator = Paginator(materials_list, 10)
        try:
            materials = paginator.page(page)
        except PageNotAnInteger:
            materials = paginator.page(1)
        except EmptyPage:
            materials = paginator.page(paginator.num_pages) 


        page = request.GET.get('page', 1)

        paginator = Paginator(stock_list, 10)
        try:
            stocks = paginator.page(page)
        except PageNotAnInteger:
            stocks = paginator.page(1)
        except EmptyPage:
            stocks = paginator.page(paginator.num_pages)    
        context = {
            'materials':materials,
            'site':site,
            'stocks':stocks
        }
              
        # Site
        # SiteMaterialCounts
        # SiteMaterialUse
        # SiteStockCounts
        # SiteStockUse
        return render(request, 'site_home.html', context)
    return redirect('home')    

@login_required 
def branch_home(request):
    if request.user.is_staff or request.user.is_branch_staff:
        user=request.user

        branch=Branch.objects.get(manager=user)

        materials_list = BranchMaterialCounts.objects.filter(branch=branch).order_by('-id')
        stock_list = BranchStockCounts.objects.filter(branch=branch).order_by('-id')

        page = request.GET.get('page', 1)

        paginator = Paginator(materials_list, 10)
        try:
            materials = paginator.page(page)
        except PageNotAnInteger:
            materials = paginator.page(1)
        except EmptyPage:
            materials = paginator.page(paginator.num_pages) 

        page = request.GET.get('page', 1)

        paginator = Paginator(stock_list, 10)
        try:
            stocks = paginator.page(page)
        except PageNotAnInteger:
            stocks = paginator.page(1)
        except EmptyPage:
            stocks = paginator.page(paginator.num_pages) 
        context = {
            'materials':materials,
            'branch':branch,
            'stocks':stocks
        }
         
        # BranchStockCounts
        # BranchStockSale
        # Branch
        # BranchMaterialCounts
        # BranchMaterialSale    
        return render(request, 'branch_home.html',context)
    return redirect('home')    


def material_sales_report(request):
    stock_list = BranchStockSale.objects.all().order_by('-id')

    material_list = MaterialSale.objects.all().order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(material_list, 10)
    try:
        materials = paginator.page(page)
    except PageNotAnInteger:
        materials = paginator.page(1)
    except EmptyPage:
        materials = paginator.page(paginator.num_pages) 

    page = request.GET.get('page', 1)

    paginator = Paginator(stock_list, 10)
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        stocks = paginator.page(1)
    except EmptyPage:
        stocks = paginator.page(paginator.num_pages)     
    context = {
        'materials':materials,
        'stocks':stocks
    }
    return render(request, 'material_sales.html', context)

# is_dispatch_staff