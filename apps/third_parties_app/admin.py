from django.contrib import admin
from django.utils.translation import gettext as _

from apps.third_parties_app.models.bank import Bank
from apps.third_parties_app.models.city import City


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
                    'tax_rate'
                ]
            }
        )
    )
    list_display = ('city_name', 'joppd', 'tax_rate')


class BankAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _('Bank data'), {
                "fields": [
                    'oib',
                    'bank_name'
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
        )
    )
    list_display = ('bank_name', 'oib', 'city_name')


admin.site.register(City, CityAdmin)
admin.site.register(Bank, BankAdmin)
