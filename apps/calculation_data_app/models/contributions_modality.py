from django.db import models
from django.utils.translation import gettext_lazy as _


class ContributionsModality(models.Model):
    
    class Meta:
        verbose_name = _('Contributions model')
        verbose_name_plural = _('Contributions models')

    modality_mark = models.CharField(
        verbose_name=_('Modality mark'), unique=True, max_length=10, help_text=_('Up to 10 characters long textual ID of this modality'))

    pension_fund_min_base = models.FloatField(
        verbose_name=_('Pension fund minimal base'), help_text=_("The year's legal minimum pension fund base. Use '.' as decimal point"), default=3321.96)

    pension_fund_gen = models.FloatField(
        verbose_name=_('Pension fund - generational'), default=0.15, help_text=_('Legal rate for the generational pension fund. Expressed as a decimal number'))
    pension_fund_ind = models.FloatField(
        verbose_name=_('Pension fund - individual'), default=0.05, help_text=_('Legal rate for the individual pension fund. Expressed as a decimal number'), null=True)

    health_insurance = models.FloatField(
        verbose_name=_('Health fund'), default=0.165, help_text=_('Legal rate for the health insurance fund. Expressed as a decimal number'), null=True)


    def __str__(self):
        return f"{self.modality_mark}"
