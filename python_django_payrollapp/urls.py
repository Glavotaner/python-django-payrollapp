"""python_django_payrollapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.payroll_app import views
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('', views.select_period, name='select_period'),
    path('admin/', admin.site.urls),
    path('payroll/', include('apps.payroll_app.urls', namespace='payroll')),
    path('employees_Y<int:year>M<int:month>D<str:accounting_date>',
         views.process_payroll, name='process_payroll'),
    path('payrolls_Y<int:year>M<int:month>',
         views.payrolls_processed, name='processed_payrolls'),
    path('payroll_detail_ID<int:payroll_id>',
         views.payroll_detail, name='payroll_detail'),
]
