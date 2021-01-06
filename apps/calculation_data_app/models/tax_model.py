from django.db import models
from django.utils.translation import gettext_lazy as _

class TaxModel(models.Model):
    
    class Meta:
        verbose_name = _('Tax model')
        verbose_name_plural = _('Tax models')
        
    tax_from = models.FloatField(verbose_name=_("Tax from"))
    tax_to = models.FloatField(verbose_name=_("Tax to"))
    
    tax_rate = models.FloatField(verbose_name=_("Tax rate"), help_text=_("Expressed as a decimal number"))

    
    def __str__(self):
        return f"{self.tax_rate}"