from django.shortcuts import render
from stocks.models import Damage
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    return render(request, 'index.html')


def damages_report(request):  
    damages_list = Damage.objects.all().order_by('-id')
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
    }  
    return render(request, 'damages.html', context)
