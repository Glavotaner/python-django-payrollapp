from django.contrib import admin
from .models.bank import Bank
from .models.city import City


class BankAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            'Bank data', {
                "fields": [
                    'business_id',
                    'oib',
                    'bank_name'
                ],
            }),
        (
            'Address and contact data', {
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
            'City data', {
                "fields": [
                    'city_name',
                    'postal_code',
                    'iban'
                ],
            }),
        (
            'Tax data', {
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
