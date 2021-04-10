from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class HourType(models.Model):
    hour_type_id = models.AutoField(primary_key=True)

    hour_type_name = models.CharField(max_length=250, verbose_name=_('Hour type name'))

    retired = models.BooleanField(verbose_name=_('Retired'))

    @staticmethod
    def get_current_hour_types() -> List['HourType']:
        return HourType.objects.filter(retired=True)

    class Meta:
        verbose_name = 'Hour type'
        verbose_name_plural = 'Hour types'

        db_table = 'hour_types'
