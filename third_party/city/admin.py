from django.contrib import admin

from third_party.city.models import City

class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'iban', 'tax_rate')

admin.site.register(City, CityAdmin)
