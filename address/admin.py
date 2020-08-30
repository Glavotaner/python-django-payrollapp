from django.contrib import admin
from .models import EmployeeAddress, BankAddress


admin.site.register(EmployeeAddress)
admin.site.register(BankAddress)