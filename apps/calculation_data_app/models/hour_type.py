from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


# from apps.calculation_data_app.models import HourTypeCoef


class HourType(models.Model):
    hour_type_id = models.AutoField(primary_key=True)
    hour_type_name = models.CharField(max_length=250, verbose_name=_('Hour type name'))
    retired = models.BooleanField(verbose_name=_('Retired'))

    class Meta:
        verbose_name = 'Hour type'
        verbose_name_plural = 'Hour types'

        db_table = 'hour_types'

    @staticmethod
    def get_current_hour_types() -> List['HourType']:
        return HourType.objects.filter(retired=False)

    @property
    def html_id(self):
        return f'{self.hour_type_id}id_hour_type'

    # def get_hour_coef_for_date(self, target_date: date) -> HourTypeCoef:
    #   return HourTypeCoef.objects.filter(hour_type=self, valid_from__lte=target_date).order_by('valid_from').get()
