from django.contrib import admin

from .models import TaxModel, HourFund, ContributionsModel, DeductiblesModel, TaxBreakModel, ContributionPercentage, \
    Contribution


class TaxModelAdmin(admin.ModelAdmin):
    list_display = ('tax_from', 'tax_to', 'tax_rate')


class TaxBreakModelAdmin(admin.ModelAdmin):
    list_display = ('description', 'tax_break')


class HourFundAdmin(admin.ModelAdmin):
    list_display = ('period_id', 'year', 'month', 'total_hours')


class DeductibleAdmin(admin.ModelAdmin):
    list_display = ('base_deductible', 'personal_deductible_coef', 'valid_from')


class ContributionAdmin(admin.ModelAdmin):
    fields = ('name', 'out_of_pay', 'retired_from')


class ContributionPercentageAdmin(admin.ModelAdmin):
    fields = ('contribution', 'percentage')


class ContributionsModelAdmin(admin.ModelAdmin):
    fields = ('model_mark', 'contributions')


admin.site.register(TaxModel, TaxModelAdmin)
admin.site.register(TaxBreakModel, TaxBreakModelAdmin)
admin.site.register(HourFund, HourFundAdmin)
admin.site.register(Contribution, ContributionAdmin)
admin.site.register(ContributionPercentage, ContributionPercentageAdmin)
admin.site.register(ContributionsModel, ContributionsModelAdmin)
admin.site.register(DeductiblesModel, DeductibleAdmin)
