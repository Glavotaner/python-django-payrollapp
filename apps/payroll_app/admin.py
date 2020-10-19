from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Labour, Payroll


class LabourAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None, {
                "fields": [
                    'employee'
                ],
        }),
        (
            _('Accounted period data'), {
                'fields': [
                    'labour_start_date',
                    'labour_end_date'
                ]
            }
        ),
        (
            _('Accounted hours data'), {
                'fields': [
                    'regular_hours',
                    'overtime_hours',
                    'special_hours'
                ]
            }
        )
    )
    
    
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('months_hours_fund', 'gross_salary', 'health_insurance_amount', 'pension_fund_total', 'income', 'personal_deductible_amount', 'deductibles', 'tax_base', 'income_tax_amount', 'city_tax_amount', 'tax_amount', 'net_salary')
    
    fieldsets = (
        (
            _('Accounted period data'), {
                'fields': [
                    'accounted_period_start',
                    'accounted_period_end'
                ]
            }
        ),
        (
            _('Employee and labour data'), {
                'fields': [
                    'employee',
                    'work_data'
                ]
            }
        )
    )


admin.site.register(Labour, LabourAdmin)
admin.site.register(Payroll, PayrollAdmin)