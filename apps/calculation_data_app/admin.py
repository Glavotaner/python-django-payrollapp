from django.contrib import admin

from .models import TaxModel, HourFund, ContributionsModel, DeductiblesModel


class TaxModelAdmin(admin.ModelAdmin):
    list_display = ('tax_from', 'tax_to', 'tax_rate')


class HourFundAdmin(admin.ModelAdmin):
    list_display = ('period_id', 'year', 'month', 'total_hours')


class DeductibleAdmin(admin.ModelAdmin):
    list_display = ('base_deductible', 'personal_deductible_coef', 'valid_from')


class ContributionsModalityAdmin(admin.ModelAdmin):
    list_display = ('model_mark', 'min_base', 'pension_fund_gen', 'pension_fund_ind', 'health_insurance')


admin.site.register(TaxModel, TaxModelAdmin)
admin.site.register(HourFund, HourFundAdmin)
admin.site.register(ContributionsModel, ContributionsModalityAdmin)
admin.site.register(DeductiblesModel, DeductibleAdmin)
