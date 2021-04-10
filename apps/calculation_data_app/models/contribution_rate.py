from datetime import date
from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import Contribution


class ContributionRate(models.Model):

    contribution_rate_id = models.AutoField(primary_key=True)

    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE, verbose_name=_('Contribution'))
    rate = models.FloatField(default=0, verbose_name=_('Rate'))

    valid_from = models.DateField(verbose_name=_('Valid from'))

    @property
    def contribution_name(self):
        return self.contribution.contribution_name

    @staticmethod
    def get_valid_contribution_rates(target_date: date) -> List['ContributionRate']:
        return ContributionRate.objects.raw("""SELECT * FROM contribution_rates 
                                            WHERE valid_from = (SELECT MAX(valid_from) FROM contribution_rates
                                            WHERE valid_from <= %s)""", target_date)

    class Meta:
        verbose_name = _('Contribution rate')
        verbose_name_plural = _('Contribution rates')

        db_table = 'contribution_rates'

    def __str__(self):
        return f"{self.contribution_name}: {str(self.rate)}%"
