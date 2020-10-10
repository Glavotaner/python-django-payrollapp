from django.contrib import admin

from .models import City

class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'iban', 'tax_rate')
    
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
    
admin.site.register(City, CityAdmin)
