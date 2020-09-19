from django.contrib import admin

from .models import Address, Person


class _ModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}
    
class PersonAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        return {}

    list_display = ('pid', 'disability', 'first_name', 'last_name', 'date_of_birth', 'age')

    field_sets = [("Personal", {"fields": (("pid", "first_name", "last_name", "date_of_birth", "age"))})]

admin.site.register(Address, _ModelAdmin)
admin.site.register(Person, PersonAdmin)