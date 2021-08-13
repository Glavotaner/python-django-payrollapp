from django.db import models
from django.utils.translation import gettext_lazy as _


class TaxBreak(models.Model):
    tax_break_id = models.AutoField(primary_key=True)
    tax_break_name = models.CharField(
        max_length=250, verbose_name=_('Tax break name'))
    rate = models.FloatField(verbose_name=_('Rate'), default=50)
    retired = models.BooleanField(verbose_name=_('Retired'))

    class Meta:
        verbose_name = _('Tax break')
        verbose_name_plural = _('Tax breaks')

        db_table = 'tax_breaks'

    def __str__(self):
        return f"{self.tax_break_name}"

    @staticmethod
    def get_valid_tax_breaks():
        return TaxBreak.objects.filter(retired=False)
