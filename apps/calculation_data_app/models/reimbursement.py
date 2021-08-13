from typing import Dict, List
from datetime import date

from django.db import models
from django.db.models.query import RawQuerySet
from django.utils.translation import gettext_lazy as _


class Reimbursement(models.Model):
    reimbursement_id = models.AutoField(primary_key=True)
    reimbursement_name = models.CharField(
        max_length=120, verbose_name=_('Reimbursement name'))
    retired = models.BooleanField(verbose_name=_('Retired'))

    class Meta:
        verbose_name = _('Reimbursement')
        verbose_name_plural = _('Reimbursements')

        db_table = 'reimbursements'

    def __str__(self):
        return f'{self.reimbursement_name}'

    @staticmethod
    def get_valid_reimbursements(target_date: date) -> RawQuerySet:
        return Reimbursement.objects.raw("""
        SELECT r.*, rv.amount FROM reimbursements as r
        LEFT JOIN (
            SELECT MAX(valid_from) AS max_date, reimbursement_id FROM Reimbursement_values
            WHERE valid_from <= %s OR valid_from IS NULL
            GROUP BY reimbursement_id
            ) AS max_date ON max_date.reimbursement_id = r.reimbursement_id
        LEFT JOIN reimbursement_values AS rv 
        ON rv.reimbursement_id = max_date.reimbursement_id AND rv.valid_from = max_date.max_date
        WHERE COALESCE(r.retired, 0) = 0
        """, [target_date])

    @property
    def html_id(self):
        return f'{self.reimbursement_id}id_reimbursement'
