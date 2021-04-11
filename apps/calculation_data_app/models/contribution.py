from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class Contribution(models.Model):

    contribution_id = models.AutoField(primary_key=True)
    contribution_name = models.CharField(max_length=120, verbose_name=_('Name'), unique=True)
    out_of_pay = models.BooleanField(default=True, verbose_name=_('Out of pay'))
    retired = models.BooleanField(verbose_name=_('Retired'))

    class Meta:
        verbose_name = _('Contribution')
        verbose_name_plural = _('Contributions')

        db_table = 'contributions'

    def __str__(self):
        return f"{self.contribution_name}"

    @staticmethod
    def get_current_contributions() -> List['Contribution']:
        return Contribution.objects.filter(retired=True)

