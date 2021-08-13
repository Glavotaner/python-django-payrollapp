from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import Contribution


class ContributionAmount(models.Model):
    contribution_amount_id = models.AutoField(primary_key=True)

    contribution = models.ForeignKey(Contribution, on_delete=models.PROTECT, verbose_name=_('Contribution'))
    payroll = models.ForeignKey('Payroll', on_delete=models.PROTECT, verbose_name=_('Payroll'))

    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, editable=False, verbose_name=_('Amount'))

    class Meta:
        verbose_name = _('Contribution amount')
        verbose_name_plural = _('Contribution amounts')

        db_table = 'contribution_amounts'

    def __str__(self):
        return f'{self.contribution.contribution_name} - {self.amount}'

    @staticmethod
    def get_payroll_contribution_amounts(target_payroll_id: int):
        return ContributionAmount.objects.filter(payroll__payroll_id=target_payroll_id)

    @property
    def contribution_name(self):
        return self.contribution.contribution_name

    @property
    def contribution_rate(self):
        if self.contribution.from_pay:
            return round(self.amount / self.payroll.contributions_base * 100, 2)
        else:
            return round(self.amount / self.payroll.gross_salary * 100, 2)
