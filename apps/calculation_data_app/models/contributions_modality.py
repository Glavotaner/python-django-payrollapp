from django.db import models
from django.db.models.query_utils import Q

class ContributionsModality(models.Model):
    
    modality_mark = models.CharField(verbose_name = 'Modality mark', unique=True, max_length = 10)
    
    pension_fund_min_base = models.FloatField(verbose_name='Pension fund minimal base')
    
    pension_fund_gen = models.FloatField(verbose_name = 'Pension fund 1', default=0.15)
    pension_fund_ind = models.FloatField(verbose_name = 'Pension fund 2', default=0.05)
    
    health_insurance = models.FloatField(verbose_name = 'Health fund', default = 0.165)
    
    class Meta:
        
        constraints = [
            models.CheckConstraint(check=Q(pension_fund_min_base__gte=0), name='pension_min_base_gte_0'),
            models.CheckConstraint(check=Q(pension_fund_gen__gte=0), name='pension_fund_gen_gte_0'),
            models.CheckConstraint(check=Q(pension_fund_ind__gte=0), name='pension_fund_ind_gte_0')    
        ]
    
    def __str__(self):
        return f"{self.modality_mark}"