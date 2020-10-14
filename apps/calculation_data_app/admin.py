from django.contrib import admin

from .models import TaxModel, HourFund, ContributionsModality, Deductible

admin.site.register(TaxModel)
admin.site.register(HourFund)
admin.site.register(ContributionsModality)
admin.site.register(Deductible)
