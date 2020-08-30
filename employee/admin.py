from django.contrib import admin

from employee.models import  PaymentInfo, Deductibles, Employee


admin.site.register(PaymentInfo)
admin.site.register(Deductibles)
admin.site.register(Employee)
