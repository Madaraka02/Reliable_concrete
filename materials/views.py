from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from production.models import *
from .utils import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime, date, timedelta
from django.db.models import Q

# from datetime import date

# today = date.today()

# # dd/mm/YY
# d1 = today.strftime("%d/%m/%Y")


month = datetime.now().month
year = datetime.now().year

# Create your views here.
current_date = datetime.today()
def material_report(request):
    materials = RawMaterial.objects.all()    
    raw_materials = Moulding.objects.all() 
    materials_list = RawMaterial.objects.all().order_by('-id')

    # materials = CuringStock.objects.all().order_by('-id')
    x= [x.name for x in materials_list]
    y= [y.available_qty for y in materials_list]
    chart = get_plot(x, y)   
    # pie = get_pie(x, y) 
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
        'chart':chart,
        # 'pie':pie
    }
    return render(request, 'materials.html', context)

def update_material(request, id):
    material = get_object_or_404(RawMaterial, id=id)
    qty_in_stock= material.available_qty
    bought_earlier = material.quantity
    form = MaterialForm(instance=material)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            bought = int(form.data['quantity'])
            amt_paid = int(form.data['amount'])
            material = form.save(commit=False)
            updated = qty_in_stock + bought
            qty_bought= bought + bought_earlier
            material.available_qty = updated
            material.quantity = qty_bought

            timestamped = TimeStampedMaterialUpdate.objects.create(material=material,quantity=bought,amount_paid=amt_paid,date=current_date)
            timestamped.save()
            material_count = MaterialCounts.objects.get(material=material)
            material_count.quantity +=bought
            material_count.save()
            material.save()
            # print(f'instock {updated}')
            # print(f'Boughtupdates {qty_bought}')

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
            qty = int(form.data['quantity'])
            material = form.save(commit=False)
            material.available_qty = material.quantity
            material.save() 

            material_count = MaterialCounts.objects.create(material=material,quantity=qty,date=current_date)
            material_count.save()

            return redirect('add_material')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  
    #  productions = Production.objects.filter(date__month='9')   


def dispatch_material_to_branch(request):
    form = DispatchMaterialExternalForm()
    if request.method == 'POST':
        form = DispatchMaterialExternalForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])
            raw_material = form.data['material']
            to_branch = form.data['to']

            material_dispatch = form.save()


            # r_material = RawMaterial.objects.get(id=raw_material,confirm_received=True)
            r_material = get_object_or_404(RawMaterial,id=raw_material)

            print(r_material)
    
            material_count = get_object_or_404(MaterialCounts, material=r_material)
            count_qty=material_count.quantity
            updated_qty=0
            if count_qty > qty:
                updated_qty=count_qty-qty
            else:
                return redirect('store_home')    

                
            material_count.quantity=updated_qty
            material_count.save()

            

            branch = get_object_or_404(Branch, id=to_branch) #get branch
            branchh_material = BranchMaterialCounts.objects.get(material=raw_material, branch=to_branch) #get branch material to get available material
             #get branch material to get available material

            qqty=branchh_material.quantity
            upqty=qqty+qty
            branchh_material.quantity=upqty

            branchh_material.save()
            r_material.quantity -=qty
            r_material.save()
            return redirect('store_home')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  



def dispatch_material_to_site(request):
    form = DispatchMaterialToSiteForm()
    if request.method == 'POST':
        form = DispatchMaterialToSiteForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])
            raw_material = form.data['material']
            to_site = form.data['to']

            material_dispatch = form.save()


            r_material = get_object_or_404(RawMaterial,id=raw_material)
            # r_material = RawMaterial.objects.get(id=raw_material)

            print(r_material)
    
            material_count = get_object_or_404(MaterialCounts, material=r_material)
            count_qty=material_count.quantity
            updated_qty=0
            if count_qty > qty:
                updated_qty=count_qty-qty
            else:
                return redirect('store_home')    
                
            material_count.quantity=updated_qty
            print(material_count)
            material_count.save()

            site = get_object_or_404(Site, id=to_site) #get site
            site_material = SiteMaterialCounts.objects.get(material=r_material, site=site) #get branch material to get available material
             #get branch material to get available material
            

            qqty=site_material.quantity
            upqty=qqty+qty
            site_material.quantity=upqty
            r_material.quantity=rqty

            site_material.save()
            rqty=r_material.quantity
            ruqty=rqty-qty
            r_material.save()


            return redirect('store_home')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  



def main_material_sale(request, id):
    material = get_object_or_404(RawMaterial,id=id)
    materiall = get_object_or_404(MaterialCounts,material=material)
    avail_qty =materiall.quantity

    form = MainMaterialSaleForm()
    if request.method == 'POST':
        form = MainMaterialSaleForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])
            
            if avail_qty > qty:

                main_material_sale = form.save(commit=False)
                main_material_sale.sale_by='R.C.W Main'
                main_material_sale.date=current_date
                main_material_sale.save()
            else:
                return redirect('store_home')    
            
            upqty=avail_qty-qty
            materiall.quantity=upqty
            materiall.save()

            mat_qty=material.quantity
            matupqty=mat_qty-qty
            material.quantity=matupqty
            material.save()

            return redirect('store_home')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context) 

def branch_material_sale(request, id):
    branch_material = get_object_or_404(BranchMaterialCounts,id=id)
    user=request.user
    branch=Branch.objects.get(manager=user)

    form = BranchMaterialSaleForm()
    if request.method == 'POST':
        form = BranchMaterialSaleForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])
            # materiall = get_object_or_404(MaterialCounts,material=materia)
            # branch_mateial = BranchMaterialCounts.objects.get(branch=branch, material=material) #get branch material to get available material

            avail_qty =branch_material.quantity
            if avail_qty > qty:

                branch_material_sale = form.save(commit=False)
                branch_material_sale.sale_by=branch.name
                branch_material_sale.date=current_date
                branch_material_sale.material=branch_material.material
                branch_material_sale.save()
            else:
                # create request to main site for additional materials
                return redirect('branch_home')    
            

            qqty=branch_material.quantity
            upqty=avail_qty-qty
            branch_material.quantity=upqty

            # print(branch.name)
            branch_material.save()

            return redirect('branch_home')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  
# 

def site_material_use(request, id):
    material=get_object_or_404(RawMaterial, id=id)
    user=request.user
    site=Site.objects.get(manager=user)


    form = SiteMaterialUseForm()
    if request.method == 'POST':
        form = SiteMaterialUseForm(request.POST)
        if form.is_valid():
            qty = int(form.data['quantity'])

            material_use = form.save(commit=False)
            material_use.site=site
            material_use.material=material
            material_use.save()

    
            material_count = SiteMaterialCounts.objects.get(material=material, site=site)
            count_qty=material_count.quantity
            updated_qty=0
            if count_qty > qty:
                updated_qty=count_qty-qty
            else:
                return redirect('site_home')    
                
            material_count.quantity=updated_qty
            print(material_count)
            material_count.save()

            return redirect('site_home')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  

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


def export_material_usage_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="material_usage.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Stocks')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    

    columns = ['Name', 'Quantity','Date',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = RawMaterialUsage.objects.filter(date__month=month).values_list('material__name', 'quantity', 'date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response        


    
def update_material_use(request, id):
    raw_material = get_object_or_404(RawMaterialUsage, id=id)
    form = MaterialUseForm(instance=raw_material)
    if request.method == 'POST':
        form = MaterialUseForm(request.POST, instance=raw_material)
        if form.is_valid():
            form.save()

            return redirect('material_report')
    context = {
        'form':form,
        'raw_material':raw_material
        
    }        
    return render(request, 'form.html',context)  



def confirm_material_receive(request, id):
    material = get_object_or_404(RawMaterial, id=id)
    if material.confirm_received==False:
        material.confirm_received=True
        material.save()
        return redirect('material_report')

    return render(request, 'materials.html')

def add_material_use(request):
    form = MaterialUseForm()
    if request.method == 'POST':
        form = MaterialUseForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('add_material')
    context = {
        'form':form,
        
    }        
    return render(request, 'form.html',context)  