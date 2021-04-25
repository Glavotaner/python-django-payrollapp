from datetime import date
from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models.hour_type import HourType


class HourTypeCoef(models.Model):
    hour_type_coef_id = models.AutoField(primary_key=True)
    hour_type = models.ForeignKey(HourType, on_delete=models.CASCADE, verbose_name=_('Hour type'))
    coef = models.FloatField(verbose_name=_('Hour coefficient'))
    valid_from = models.DateField(verbose_name=_('Valid from'))

    class Meta:
        verbose_name = _('Hour type coef.')
        verbose_name_plural = _('Hour type coefs.')

        db_table = 'hour_type_coefs'

    def __str__(self):
        return f'{self.hour_type_name} - {self.coef}'

    @staticmethod
    def get_valid_hour_type_coefs(target_date: date) -> List['HourTypeCoef']:
        return HourTypeCoef.objects.raw("""SELECT * FROM hour_type_coefs 
                                                WHERE valid_from = (SELECT MAX(valid_from) FROM hour_type_coefs
                                                WHERE valid_from <= %s)""", target_date)

    @property
    def hour_type_name(self):
        return self.hour_type.hour_type_name
