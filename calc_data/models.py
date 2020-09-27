from django.db import models


class Deductible(models.Model):
    
    class Meta:
        get_latest_by = 'valid_from'
    
    base_deductible = models.FloatField(verbose_name='Base deductible')
    personal_deductible_coef = models.FloatField(verbose_name='Personal deductible coef')
    valid_from = models.DateTimeField(verbose_name='Valid from', auto_now=True)
    
    def __str__(self):
        return f"{self.base_deductible} | {self.personal_deductible_coef} || {self.valid_from}"      
    



class TaxModel(models.Model):
    
    class Meta:
        get_latest_by = 'valid_from'
    
    tax_bracket = models.FloatField(verbose_name = 'High tax bracket')
    lo_tax_rate = models.FloatField(verbose_name = 'Low tax rate')
    hi_tax_rate = models.FloatField(verbose_name = 'High tax rate')
    
    valid_from = models.DateField(verbose_name = 'Valid from')
    
    def __str__(self):
        return f"{self.lo_tax_rate}"
  
    

class ContributionsModality(models.Model):
    
    modality_mark = models.CharField(verbose_name = 'Modality mark', unique=True, max_length = 4)
    
    pension_fund_min_base = models.FloatField(verbose_name='Pension fund minimal base')
    
    pension_fund_gen = models.FloatField(verbose_name = 'Pension fund 1', default=0.15)
    pension_fund_ind = models.FloatField(verbose_name = 'Pension fund 2', default=0.05)
    
    health_insurance = models.FloatField(verbose_name = 'Health fund', default = 0.165)
    
    
    def __str__(self):
        return f"{self.modality_mark}"
    
    
    
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
    
