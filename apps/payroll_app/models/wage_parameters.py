from datetime import date
from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class WageParameters(models.Model):
    wage_parameters_id = models.AutoField(primary_key=True)

    min_base = models.FloatField(
        verbose_name=_('Contributions minimal base'),
        help_text=_("The year's legal minimum contributions base. Use '.' as decimal point"),
        default=3321.96
    )

    max_base = models.FloatField(
        verbose_name=_('Contributions maximum base'),
        help_text=_("The year's legal maximum contributions base. Use '.' as decimal point"),
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
    def get_valid_wage_parameters(target_date: date) -> List['WageParameters']:
        return WageParameters.objects.filter(valid_from__lte=target_date).latest()
