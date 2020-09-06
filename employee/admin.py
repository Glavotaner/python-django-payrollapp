from django.contrib import admin

from employee.models import  PaymentInfo, Employee, FamilyMember


admin.site.register(PaymentInfo)
admin.site.register(Employee)
admin.site.register(FamilyMember)
