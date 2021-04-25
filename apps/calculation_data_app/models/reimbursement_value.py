from datetime import date
from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import Reimbursement


class ReimbursementValue(models.Model):
    reimbursement_value_id = models.AutoField(primary_key=True)
    reimbursement = models.ForeignKey(Reimbursement, on_delete=models.CASCADE, verbose_name=_('Reimbursement'))
    amount = models.FloatField(verbose_name=_('Amount'))
    valid_from = models.DateField(verbose_name=_('Valid from'))

    class Meta:
        verbose_name = _('Reimbursement value')
        verbose_name_plural = _('Reimbursement values')

        db_table = 'reimbursement_values'

        get_latest_by = 'valid_from'

    def __str__(self):
        return f'{self.reimbursement_name}: {self.amount}'

    @staticmethod
    def get_valid_reimbursement_values(target_date: date) -> List['ReimbursementValue']:
        return ReimbursementValue.objects.raw("""SELECT * FROM reimbursement_values 
                                                    WHERE valid_from = (SELECT MAX(valid_from) FROM reimbursement_values
                                                    WHERE valid_from <= %s)""", target_date)

    @property
    def reimbursement_name(self):
        return self.reimbursement.reimbursement_name
