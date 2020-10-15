from django.contrib import admin

from .models import TaxModel, HourFund, ContributionsModality, Deductible

class TaxModelAdmin(admin.ModelAdmin):
    list_display = ('tax_bracket', 'lo_tax_rate', 'hi_tax_rate', 'valid_from')


class HourFundAdmin(admin.ModelAdmin):
    list_display = ('period_id', 'year', 'month', 'total_hours')


class DeductibleAdmin(admin.ModelAdmin):
    list_display = ('base_deductible', 'personal_deductible_coef', 'valid_from')


class ContributionsModalityAdmin(admin.ModelAdmin):
    list_display = ('modality_mark', 'pension_fund_min_base', 'pension_fund_gen', 'pension_fund_ind', 'health_insurance')


admin.site.register(TaxModel, TaxModelAdmin)
admin.site.register(HourFund, HourFundAdmin)
admin.site.register(ContributionsModality, ContributionsModalityAdmin)
admin.site.register(Deductible, DeductibleAdmin)
