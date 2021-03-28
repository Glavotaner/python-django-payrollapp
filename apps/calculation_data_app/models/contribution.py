from django.db import models
from gettext import gettext as _


class Contribution(models.Model):

    name = models.CharField(max_length=120, verbose_name=_('Name'), unique=True)

    out_of_pay = models.BooleanField(default=True)

    retired_from = models.DateField(verbose_name=_('Retired from'), null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
