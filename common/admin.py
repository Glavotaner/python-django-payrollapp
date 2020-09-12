from django.contrib import admin

from .models import Address, Person, PersonAdmin


class _ModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

admin.site.register(Address, _ModelAdmin)
admin.site.register(Person, PersonAdmin)