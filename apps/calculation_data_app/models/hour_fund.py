from django.db import models
from django.utils.translation import gettext_lazy as _

class HourFund(models.Model):
    
    class Meta:
        verbose_name = _('Hour fund')
        verbose_name_plural = _('Hour funds')
    

    period_id = models.IntegerField(verbose_name=_('Period ID'), unique = True, editable= False)
    year = models.IntegerField(verbose_name = _('Year'), default= 2020)
    month = models.IntegerField(verbose_name = _('Month'))
    total_hours = models.IntegerField(verbose_name = _('Total hours'))

    
    def save(self):
        self.period_id = str(self.year) + str(self.month)
        super(HourFund, self).save()
    
    def __str__(self):
        return f"{self.period_id}"