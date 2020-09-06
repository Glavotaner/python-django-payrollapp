from django.contrib import admin

from .models import BankAddress, PersonalAddress, Person


admin.site.register(BankAddress)
admin.site.register(PersonalAddress)
admin.site.register(Person)