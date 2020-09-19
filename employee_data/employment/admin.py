from django.contrib import admin

from .models import Position, Contract, SignedContract


class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_name', 'salary')

admin.site.register(Position, PositionAdmin)
admin.site.register(Contract)
admin.site.register(SignedContract)