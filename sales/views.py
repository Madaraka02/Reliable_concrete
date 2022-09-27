from django.shortcuts import render
from stocks.models import Damage

# Create your views here.
def home(request):
    return render(request, 'index.html')


def damages_report(request):  
    damages = Damage.objects.all().order_by('-id')
    context ={
        'damages':damages,
    }  
    return render(request, 'damages.html', context)
