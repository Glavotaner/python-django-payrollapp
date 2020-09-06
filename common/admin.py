from django.contrib import admin

from .models import BankAddress, PersonalAddress, Person


class _ModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

admin.site.register(BankAddress, _ModelAdmin)
admin.site.register(PersonalAddress, _ModelAdmin)
admin.site.register(Person, _ModelAdmin)