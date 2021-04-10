from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Employee, Dependent


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('oib', 'first_name', 'last_name', 'date_of_birth', 'employee_since', 'first_employment',
                    'first_employment_with_company', 'no_dependents', 'no_children', 'no_dependents_disabled',
                    'no_dependents_disabled_100')

    search_fields = ['oib']

    fieldsets = (
        (
            _('Personal data'), {
                "fields": [
                    'oib',
                    'first_name',
                    'last_name',
                    'date_of_birth',
                    'disability',
                    'hrvi'
                ],
            }),
        (
            _('Address and contact data'), {
                'fields': [
                    'city',
                    'street_name',
                    'street_number'
                ]
            }
        ),
        (
            _('Payment info'), {
                'fields': [
                    'employee_bank',
                    'iban',
                    'employee_protected_bank',
                    'protected_iban'
                ]
            }
        ),
        (
            _('Employment data'), {
                'fields': [
                    'first_employment',
                    'first_employment_with_company',
                    'signed_contract'
                ]
            }
        ),
        (
            'Accounting data', {
                'fields': [
                    'contributions_model',
                    'tax_breaks'
                ]
            }
        )
    )


class DependentAdmin(admin.ModelAdmin):
    fields = [
        'oib',
        'first_name',
        'last_name',
        'date_of_birth',
        'child_in_line',
        'disability',
        'dependent_of'
    ]

    search_fields = ['oib']
    list_display = ('oib', 'first_name', 'last_name', 'date_of_birth', 'child_in_line', 'disability')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Dependent, DependentAdmin)
