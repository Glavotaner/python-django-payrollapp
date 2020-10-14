from django.db import models
from django.utils.translation import gettext_lazy as _

class TaxModel(models.Model):
    
    
    tax_bracket = models.FloatField(verbose_name = _('High tax bracket'))
    lo_tax_rate = models.FloatField(verbose_name = _('Low tax rate'))
    hi_tax_rate = models.FloatField(verbose_name = _('High tax rate'))
    
    valid_from = models.DateField(verbose_name = _('Valid from'))

    class Meta:
        verbose_name = _('Tax model')
        verbose_name_plural = _('Tax models')
        get_latest_by = 'valid_from'
    
    def __str__(self):
        return f"{self.lo_tax_rate}"