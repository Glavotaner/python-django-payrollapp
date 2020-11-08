from django.db import models
from django.utils.translation import gettext_lazy as _


class Deductible(models.Model):
    
    class Meta:
        verbose_name = _('Deductible')
        verbose_name_plural = _('Deductibles')
        get_latest_by = 'valid_from'
        

    base_deductible = models.FloatField(verbose_name=_(
        'Base deductible'), help_text=_('Legal base deductible amount'), default = 2500)
    personal_deductible_coef = models.FloatField(verbose_name=_(
        'Personal deductible coef'), help_text=_('Legal personal deductible coefficient'), default = 1.6)
    valid_from = models.DateTimeField(
        verbose_name=_('Valid from'), auto_now_add=True)


    def __str__(self):
        return f"{self.base_deductible} | {self.personal_deductible_coef} || {self.valid_from}"
