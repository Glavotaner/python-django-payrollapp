from django.db import models
from django.utils.translation import gettext_lazy as _

class Position(models.Model):

    position_name = models.CharField(
        max_length=30, verbose_name = _('Position name'), unique=True)
    salary = models.FloatField(verbose_name = _('Salary'))

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')

    def __str__(self):
        return self.position_name
