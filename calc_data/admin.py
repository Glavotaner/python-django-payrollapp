from django.contrib import admin

from .models import TaxModel, HourFund, ContributionsModality

admin.site.register(TaxModel)
admin.site.register(HourFund)
admin.site.register(ContributionsModality)