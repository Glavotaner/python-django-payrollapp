from django.contrib import admin

from .models import Position, ContractType, Contract


class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_name', 'salary')


admin.site.register(Position, PositionAdmin)
admin.site.register(ContractType)
admin.site.register(Contract)
