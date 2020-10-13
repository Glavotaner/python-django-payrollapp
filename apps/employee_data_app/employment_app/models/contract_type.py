from django.db import models
from django.utils.translation import gettext_lazy as _


class ContractType(models.Model):

    contract_id = models.CharField(
        max_length=30, verbose_name = _('Contract ID'), primary_key=True)
    contract_type = models.CharField(
        max_length=30, verbose_name = _('Contract type'))

    class Meta:
        verbose_name = _('Contract type')
        verbose_name_plural = _('Contract types')

    def __str__(self):
        return self.contract_type
