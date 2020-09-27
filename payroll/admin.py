from django.contrib import admin

from payroll.models import Labour, Payroll


class LabourAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None, {
                "fields": [
                    'employee'
                ],
        }),
        (
            'Accounted period data', {
                'fields': [
                    'labour_period',
                    'labour_start_date',
                    'labour_end_date'
                ]
            }
        ),
        (
            'Accounted hours data', {
                'fields': [
                    'regular_hours',
                    'overtime_hours',
                    'special_hours'
                ]
            }
        )
    )
    
    
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('accounted_period', 'months_hours_fund', 'gross_salary', 'health_insurance_amount', 'pension_fund_total', 'income', 'personal_deductible_amount', 'deductibles', 'tax_base', 'income_tax_amount', 'city_tax_amount', 'tax_amount', 'net_salary')
    
    fieldsets = (
        (
            'Accounted period data', {
                'fields': [
                    'accounted_period_start',
                    'accounted_period_end'
                ]
            }
        ),
        (
            'Employee and labour data', {
                'fields': [
                    'employee',
                    'work_data'
                ]
            }
        )
    )


admin.site.register(Labour, LabourAdmin)
admin.site.register(Payroll, PayrollAdmin)