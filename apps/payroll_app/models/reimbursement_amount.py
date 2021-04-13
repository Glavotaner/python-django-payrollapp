from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import Reimbursement


class ReimbursementAmount(models.Model):

    reimbursement_amount_id = models.AutoField(primary_key=True)

    reimbursement = models.ForeignKey(Reimbursement, on_delete=models.PROTECT, verbose_name=_('Reimbursement'))
    payroll = models.ForeignKey('Payroll', on_delete=models.PROTECT, verbose_name=_('Payroll'))

    amount = models.FloatField(verbose_name=_('Amount'))

    class Meta:
        verbose_name = _('Reimbursement amount')
        verbose_name_plural = _('Reimbursement amounts')

        db_table = 'reimbursement_amounts'

    def __str__(self):
        return f'{self.reimbursement.reimbursement_name} - {self.amount}'

    @staticmethod
    def get_payroll_reimbursement_amounts(target_payroll):
        return ReimbursementAmount.objects.filter(payroll=target_payroll)

    @property
    def reimbursement_name(self):
        return self.reimbursement.reimbursement_name
