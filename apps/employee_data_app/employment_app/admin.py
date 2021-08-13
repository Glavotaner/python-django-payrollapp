from django.contrib import admin

from .models import Position, ContractType, Contract


class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_name', 'salary', 'retired')


class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ('contract_type_name', 'retired')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_type_name', 'position_name',
                    'total_salary', 'start_date', 'end_date')


admin.site.register(Position, PositionAdmin)
admin.site.register(ContractType, ContractTypeAdmin)
admin.site.register(Contract, ContractAdmin)
