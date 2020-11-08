from django.db import models
from django.utils.translation import gettext_lazy as _

class TaxModel(models.Model):
    
    class Meta:
        verbose_name = _('Tax model')
        verbose_name_plural = _('Tax models')
        get_latest_by = 'valid_from'
    
    
    tax_bracket = models.FloatField(verbose_name = _('High tax bracket'), default = 30000)
    lo_tax_rate = models.FloatField(verbose_name = _('Low tax rate'), default = 0.24)
    hi_tax_rate = models.FloatField(verbose_name = _('High tax rate'), default = 0.36)
    
    valid_from = models.DateField(verbose_name = _('Valid from'))

    
    def __str__(self):
        return f"{self.lo_tax_rate}"