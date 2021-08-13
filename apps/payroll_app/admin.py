from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Labour, Payroll, WageParameters


class WageParametersAdmin(admin.ModelAdmin):
    fields = (
        'min_wage',
        'min_base',
        'max_base',
        'valid_from'
    )

    list_display = (
        'min_wage',
        'min_base',
        'max_base',
        'valid_from'
    )


class LabourAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'employee')
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
                    'year',
                    'month'
                ]
            }
        ),
        (
            _('Accounted hours data'), {
                'fields': [
                    'regular_hours',
                ]
            }
        )
    )


class PayrollAdmin(admin.ModelAdmin):
    list_display = ('gross_salary', 'contributions_frompay_total', 'income',
                    'personal_deductible_amount', 'total_deductibles', 'tax_base', 'income_tax_amount',
                    'city_tax_amount', 'total_tax', 'net_salary', 'reimbursements_total', 'contributions_other_total')

    fieldsets = (
        (
            _('Accounted period data'), {
                'fields': [
                    'date_of_accounting'
                ]
            }
        ),
        (
            _('Employee and labour data'), {
                'fields': [
                    'work_data'
                ]
            }
        ),
        (
            _('Payroll components'), {
                'fields': [
                    'gross_salary', 'contributions_frompay_total', 'income',
                    'personal_deductible_amount', 'total_deductibles', 'tax_base', 'income_tax_amount',
                    'city_tax_amount', 'total_tax', 'net_salary', 'reimbursements_total', 'contributions_other_total'
                ]
            }
        )
    )


admin.site.register(Labour, LabourAdmin)
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(WageParameters, WageParametersAdmin)
