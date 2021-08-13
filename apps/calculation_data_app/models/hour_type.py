from typing import List

from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _


class HourType(models.Model):
    hour_type_id = models.AutoField(primary_key=True)
    hour_type_name = models.CharField(
        max_length=250, verbose_name=_('Hour type name'))
    retired = models.BooleanField(verbose_name=_('Retired'))

    def __str__(self) -> str:
        return self.hour_type_name

    class Meta:
        verbose_name = _('Hour type')
        verbose_name_plural = _('Hour types')

        db_table = 'hour_types'

    @staticmethod
    def get_current_hour_types() -> QuerySet:
        return HourType.objects.filter(retired=False)

    @property
    def html_id(self):
        return f'{self.hour_type_id}id_hour_type'
