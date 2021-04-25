from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)

    position_name = models.CharField(
        max_length=80, verbose_name=_('Position name')
    )
    salary = models.FloatField(verbose_name=_('Salary'), default=5600)

    retired = models.BooleanField()

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')

        db_table = 'positions'

    def __str__(self):
        return f'{self.position_name} - {self.salary}kn'

    @staticmethod
    def get_valid_positions() -> List['Position']:
        return Position.objects.filter(retired=False)
