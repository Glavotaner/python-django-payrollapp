from django.contrib import admin

from payroll.models import Labour, Payroll

class PayrollAdmin(admin.ModelAdmin):
    list_display = ('accounted_period', 'gross_salary', 'net_salary')

admin.site.register(Labour)
admin.site.register(Payroll, PayrollAdmin)