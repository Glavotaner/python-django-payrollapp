from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class Reimbursement(models.Model):

    reimbursement_id = models.AutoField(primary_key=True)
    reimbursement_name = models.CharField(max_length=120, verbose_name=_('Reimbursement name'))
    retired = models.BooleanField(verbose_name=_('Retired'))

    class Meta:
        verbose_name = _('Reimbursement')
        verbose_name_plural = _('Reimbursements')

        db_table = 'reimbursements'

    def __str__(self):
        return f'{self.reimbursement_name}'

    @staticmethod
    def get_valid_reimbursements() -> List['Reimbursement']:
        return Reimbursement.objects.filter(retired=False)

