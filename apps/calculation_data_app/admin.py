from django.contrib import admin

from .models import TaxBracket, HourFund, ContributionsModel, DeductiblesModel, TaxBreak, ContributionRate, \
    Contribution, HourType, HourTypeCoef, Reimbursement, ReimbursementValue


class ContributionAdmin(admin.ModelAdmin):
    fields = ('contribution_name', 'out_of_pay', 'retired')


class ContributionRateAdmin(admin.ModelAdmin):
    fields = ('rate', 'valid_from')


class ContributionsModelAdmin(admin.ModelAdmin):
    fields = ('model_mark', 'contributions')


class DeductiblesModelAdmin(admin.ModelAdmin):
    list_display = (
        'base_deductible', 'personal_deductible_coef',
        'dependent', 'disabled_dependent_i', 'disabled_dependent_i100',
        'first_child', 'second_child', 'third_child', 'fourth_child', 'fifth_child', 'sixth_child', 'seventh_child',
        'eighth_child', 'ninth_child', 'multiplication_coef',
        'valid_from'
    )


class HourFundAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'total_hours')


class HourTypeAdmin(admin.ModelAdmin):
    list_display = ('hour_type_name', 'retired')


class HourTypeCoefAdmin(admin.ModelAdmin):
    list_display = ('hour_type_name', 'coef', 'valid_from')


class TaxBracketAdmin(admin.ModelAdmin):
    list_display = ('tax_from', 'tax_to', 'tax_rate')


class TaxBreakAdmin(admin.ModelAdmin):
    list_display = ('tax_break_name', 'rate')


class ReimbursementAdmin(admin.ModelAdmin):
    list_display = ('reimbursement_name', 'retired')


class ReimbursementValueAdmin(admin.ModelAdmin):
    list_display = ('reimbursement_name', 'amount', 'valid_from')


admin.site.register(Contribution, ContributionAdmin)
admin.site.register(ContributionRate, ContributionRateAdmin)
admin.site.register(ContributionsModel, ContributionsModelAdmin)

admin.site.register(DeductiblesModel, DeductiblesModelAdmin)

admin.site.register(HourFund, HourFundAdmin)

admin.site.register(HourType, HourTypeAdmin)
admin.site.register(HourTypeCoef, HourTypeCoefAdmin)

admin.site.register(TaxBracket, TaxBracketAdmin)
admin.site.register(TaxBreak, TaxBreakAdmin)

admin.site.register(Reimbursement, ReimbursementAdmin)
admin.site.register(ReimbursementValue, ReimbursementValueAdmin)
