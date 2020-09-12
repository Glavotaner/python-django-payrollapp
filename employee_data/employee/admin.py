from django.contrib import admin

from employee_data.employee.models import  Employee, Dependent


admin.site.register(Employee)
admin.site.register(Dependent)
