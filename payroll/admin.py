from django.contrib import admin

from payroll.models import Labour, Payroll

# Register your models here.
admin.site.register(Labour)
admin.site.register(Payroll)