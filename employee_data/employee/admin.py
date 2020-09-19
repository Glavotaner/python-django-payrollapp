from django.contrib import admin

from employee_data.employee.models import  Employee, Dependent

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('pid', 'first_name', 'last_name', 'date_of_birth', 'age', 'disability', 'no_dependents','no_dependents_disabled','no_dependents_disabled_100', 'no_children')
    
    field_sets = [("Personal", {"fields": (("pid", "first_name", "last_name", "date_of_birth", "age"))})]

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Dependent)