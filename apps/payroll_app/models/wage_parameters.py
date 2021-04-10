from django.utils.translation import gettext_lazy as _
from django.db import models

from typing import List

from datetime import date


class WageParameters(models.Model):
    class Meta:
        verbose_name = _('Wage parameters model')
        verbose_name_plural = _('Wage parameters models')

        db_table = 'wage_parameters'
    
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

    @staticmethod
    def get_valid_wage_parameters(target_date: date) -> List['WageParameters']:
        return WageParameters.objects.raw("""SELECT * FROM wage_parameters 
                                                    WHERE valid_from = (SELECT MAX(valid_from) FROM wage_parameters
                                                    WHERE valid_from <= %s)""", target_date)
