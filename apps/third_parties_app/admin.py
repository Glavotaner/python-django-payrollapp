from django.contrib import admin
from django.utils.translation import gettext as _

from .models.bank import Bank
from .models.city import City


class BankAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            _('Bank data'), {
                "fields": [
                    'business_id',
                    'oib',
                    'bank_name'
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
        )
    )


class CityAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            _('City data'), {
                "fields": [
                    'city_name',
                    'postal_code',
                    'iban'
                ],
            }),
        (
            _('Tax data'), {
                'fields': [
                    'joppd',
                    'tax_rate',
                    'tax_break'
                ]
            }
        )
    )


admin.site.register(Bank, BankAdmin)
admin.site.register(City, CityAdmin)
