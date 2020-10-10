from django.db import models

class HourFund(models.Model):
    
    
    year = models.IntegerField(verbose_name='Year', default= 2020)
    month = models.IntegerField(verbose_name = 'Month')
    total_hours = models.IntegerField(verbose_name = 'Total hours')
    
    @property
    def period_id(self):
        period_year = str(self.year)
        period_month = str(self.month)
        
        return period_year + period_month
    
    def __str__(self):
        return f"{self.period_id}"