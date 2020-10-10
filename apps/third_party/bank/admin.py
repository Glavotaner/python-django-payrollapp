from django.contrib import admin
from .models import Bank

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

admin.site.register(Bank, BankAdmin)