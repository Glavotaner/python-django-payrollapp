from apps.payroll_app.models.labour import Labour
from datetime import date
from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class WageParameters(models.Model):
    wage_parameters_id = models.AutoField(primary_key=True)

    min_base = models.FloatField(
        verbose_name=_('Contributions minimal base'),
        help_text=_(
            "The year's legal minimum contributions base. Use '.' as decimal point"),
        default=3321.96
    )

    max_base = models.FloatField(
        verbose_name=_('Contributions maximum base'),
        help_text=_(
            "The year's legal maximum contributions base. Use '.' as decimal point"),
        default=55086
    )

    min_wage = models.FloatField(verbose_name=_('Minimum wage'))

    valid_from = models.DateField(verbose_name=_('Valid from'))

    class Meta:
        verbose_name = _('Wage parameters')
        verbose_name_plural = _('Wage parameters')

        db_table = 'wage_parameters'

        get_latest_by = 'valid_from'

    def __str__(self):
        return f'Valid from: {self.valid_from}'

    @staticmethod
    def get_valid_wage_parameters(target_date: date) -> 'WageParameters':
        return WageParameters.objects.filter(valid_from__lte=target_date).latest()

    def get_proportional_min_wage(self, labour_data: Labour) -> float:
        return round(
            self.min_wage *
            (labour_data.regular_hours / labour_data.get_hours_fund), 2)

    def get_proportional_min_base(self, labour_data: Labour) -> float:
        return round(
            self.min_base *
            (labour_data.regular_hours / labour_data.get_hours_fund), 2)

    def below_min_wage(self, salary: float) -> bool:
        return salary < self.min_wage

    def below_min_base(self, contributions_base: float) -> bool:
        return contributions_base < self.min_base
