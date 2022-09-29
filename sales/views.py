from django.shortcuts import render
from stocks.models import Damage
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import *
# Create your views here.
def home(request):
    return render(request, 'index.html')


def damages_report(request):  
    damages_list = Damage.objects.all().order_by('-id')
    x= [x.product.product.product.name for x in damages_list]
    y= [x.quantity_damaged for x in damages_list]
    chart = get_plot(x, y)
    page = request.GET.get('page', 1)

    paginator = Paginator(damages_list, 15)
    try:
        damages = paginator.page(page)
    except PageNotAnInteger:
        damages = paginator.page(1)
    except EmptyPage:
        damages = paginator.page(paginator.num_pages) 
    context ={
        'damages':damages,
        'chart':chart
    }  
    return render(request, 'damages.html', context)
