from django.db import models
from django.utils.translation import gettext_lazy as _

class HourFund(models.Model):
    
    
    year = models.IntegerField(verbose_name = _('Year'), default= 2020)
    month = models.IntegerField(verbose_name = _('Month'))
    total_hours = models.IntegerField(verbose_name = _('Total hours'))
    
    @property
    def period_id(self):
        period_year = str(self.year)
        period_month = str(self.month)
        
        return period_year + period_month
    
    class Meta:
        verbose_name = _('Hour fund')
        verbose_name_plural = _('Hour funds')
    
    def __str__(self):
        return f"{self.period_id}"