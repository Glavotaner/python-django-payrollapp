from django.db import models
from django.db.models.query_utils import Q
from django.utils.translation import gettext_lazy as _


class ContributionsModality(models.Model):

    modality_mark = models.CharField(
        verbose_name=_('Modality mark'), unique=True, max_length=10)

    pension_fund_min_base = models.FloatField(
        verbose_name= _('Pension fund minimal base'))

    pension_fund_gen = models.FloatField(
        verbose_name= _('Pension fund 1'), default=0.15)
    pension_fund_ind = models.FloatField(
        verbose_name= _('Pension fund 2'), default=0.05)

    health_insurance = models.FloatField(
        verbose_name= _('Health fund'), default=0.165)

    class Meta:

        verbose_name = _('Contributions model')
        verbose_name_plural = _('Contributions models')

    def __str__(self):
        return f"{self.modality_mark}"
