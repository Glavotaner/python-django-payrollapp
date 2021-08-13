from datetime import datetime
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from apps.payroll_app.forms import PeriodForm
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')
