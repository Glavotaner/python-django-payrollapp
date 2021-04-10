from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class ContractType(models.Model):
    class Meta:
        verbose_name = _('Contract type')
        verbose_name_plural = _('Contract types')

        db_table = 'contract_types'

    contract_type_id = models.AutoField(primary_key=True)

    contract_type_name = models.CharField(
        max_length=50, verbose_name=_('Contract type name'))

    retired = models.BooleanField()

    @staticmethod
    def get_valid_contract_types() -> List['ContractType']:
        return ContractType.objects.filter(retired=False)

    def __str__(self):
        return self.contract_type_name
