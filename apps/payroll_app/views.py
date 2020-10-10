from django.http import HttpResponse
from django.shortcuts import render

from .models import Payroll


def index(request):
    return HttpResponse("bruh")

def payrolls(request):
    payroll_list = Payroll.objects.get(1)
    context = {'payrolls_list': payroll_list}
    
    return render(request, 'payroll/list.html', context)