from django.contrib import admin

from employee.models import  PaymentInfo, Employee, Dependent


admin.site.register(PaymentInfo)
admin.site.register(Employee)
admin.site.register(Dependent)
