from django.contrib import admin
from django.utils.translation import gettext as _

from .models import  Employee, Dependent

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('pid', 'first_name', 'last_name', 'date_of_birth', 'age', 'disability', 'no_dependents', 'no_dependents_disabled','no_dependents_disabled_100', 'no_children')
    
    fieldsets = (
        (
            _('Personal data'), {
                "fields": [
                    'pid', 
                    'first_name',
                    'last_name',
                    'date_of_birth',
                    'disability'
                ],
        }),
        (
            _('Address and contact data'), {
                'fields': [
                    'city',
                    'street_name',
                    'street_number',
                    'phone_number'
                ]
            }
        ),
        (
            _('Payment info'), {
                'fields': [
                    'employee_bank',
                    'iban'
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
            None, {
                'fields': [
                    'contributions_model'
                ]
            }
        )
    )


class DependentAdmin(admin.ModelAdmin):
    fields = [
        'pid', 
        'first_name',
        'last_name',
        'date_of_birth',
        'disability',
        'child',
        'dependent_of'
    ]
                        


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Dependent, DependentAdmin)