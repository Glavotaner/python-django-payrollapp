from django.db import models
from gettext import gettext as _


class TaxBreakModel(models.Model):
    description = models.CharField(max_length=250, verbose_name=_('Description'), unique=True)
    tax_break = models.FloatField(default=0.5)

    def __str__(self):
        return f"{self.description}"
