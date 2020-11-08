from django.db import models
from django.utils.translation import gettext_lazy as _


class ContractType(models.Model):
    
    class Meta:
        verbose_name = _('Contract type')
        verbose_name_plural = _('Contract types')
        

    contract_id = models.IntegerField(
     verbose_name = _('Contract type ID'), primary_key=True)
    contract_type = models.CharField(
        max_length=50, verbose_name = _('Contract type'))


    def __str__(self):
        return self.contract_type
