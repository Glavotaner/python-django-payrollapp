from django.shortcuts import render

from .models import Payroll


def index(request):
    return render(request, 'index.html')

def list(request):
    idvar = Payroll.objects.get(id = 1).accounted_period
    
    context = {'payroll_id': idvar}
    
    return render(request, 'list.html', context)
