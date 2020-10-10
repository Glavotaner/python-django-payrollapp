from django.db import models


class TaxModel(models.Model):
    
    class Meta:
        get_latest_by = 'valid_from'
    
    tax_bracket = models.FloatField(verbose_name = 'High tax bracket')
    lo_tax_rate = models.FloatField(verbose_name = 'Low tax rate')
    hi_tax_rate = models.FloatField(verbose_name = 'High tax rate')
    
    valid_from = models.DateField(verbose_name = 'Valid from')
    
    def __str__(self):
        return f"{self.lo_tax_rate}"