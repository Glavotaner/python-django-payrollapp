from django.db import models

class Deductible(models.Model):
    
    class Meta:
        get_latest_by = 'valid_from'
    
    base_deductible = models.FloatField(verbose_name='Base deductible')
    personal_deductible_coef = models.FloatField(verbose_name='Personal deductible coef')
    valid_from = models.DateTimeField(verbose_name='Valid from', auto_now=True)
    
    def __str__(self):
        return f"{self.base_deductible} | {self.personal_deductible_coef} || {self.valid_from}"  