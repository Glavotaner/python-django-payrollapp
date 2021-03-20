from gettext import gettext as _

from django.db import models


class WageParametersModel(models.Model):
    class Meta:
        verbose_name = 'Wage parameters model'
        verbose_name_plural = 'Wage parameters models'

    min_wage = models.FloatField(verbose_name=_('Minimum wage'))

    night_work_coef = models.FloatField(verbose_name=_('Night work multiplication coeficient'), default=2)
    sunday_work_coef = models.FloatField(verbose_name=_('Sunday work multiplication coeficient'), default=2)
    special_work_coef = models.FloatField(verbose_name=_('Special work multiplication coeficient'), default=2)
