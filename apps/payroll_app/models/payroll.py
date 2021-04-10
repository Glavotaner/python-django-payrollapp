from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _

from .labour import Labour
from .reimbursement_amount import ReimbursementAmount
from ...calculation_data_app.models import Contribution


class Payroll(models.Model):
    class Meta:
        verbose_name = _('Payroll')
        verbose_name_plural = _('Payrolls')

        db_table = 'payrolls'

    payroll_id = models.AutoField(primary_key=True)

    date_of_accounting = models.DateField(
        verbose_name=_('Date of accounting'),
        db_index=True
    )

    work_data = models.OneToOneField(
        Labour,
        on_delete=models.DO_NOTHING,
        db_index=True,
        verbose_name=_('Work data')
    )

    valid_contributions = models.ManyToManyField(Contribution, editable=False, verbose_name=_('Valid contributions'))

    reimbursements = models.ManyToManyField(ReimbursementAmount, verbose_name=_('Reimbursements'))

    wage = models.FloatField(
        verbose_name=_('Wage'), editable=False
    )

    gross_salary = models.FloatField(
        verbose_name=_('Gross salary'), editable=False
    )

    contributions_base = models.FloatField(
        verbose_name=_('Contributions base'), editable=False
    )

    contributions_outofpay_total = models.FloatField(verbose_name=_('Total contributions out-of-pay'))

    income = models.FloatField(verbose_name=_('Income'), editable=False)

    personal_deductible_amount = models.FloatField(
        verbose_name=_('Personal deductible amount'), editable=False
    )

    deductible_dependents = models.FloatField(
        verbose_name=_('Dependents deductible amount'), editable=False
    )
    deductible_children = models.FloatField(
        verbose_name=_('Children deductible amount'), editable=False
    )
    deductible_dependents_disabled = models.FloatField(
        verbose_name=_('Disabled dependents deductible amount'), editable=False
    )
    deductible_dependents_disabled_100 = models.FloatField(
        verbose_name=_('100% disabled dependents deductible amount'),
        editable=False
    )
    total_deductibles = models.FloatField(
        verbose_name=_('Total deductibles amount'), editable=False
    )

    tax_base = models.FloatField(verbose_name=_('Tax base'), editable=False)

    income_tax_amount = models.FloatField(
        verbose_name=_('Income tax amount'), editable=False
    )
    city_tax_amount = models.FloatField(
        verbose_name=_('City tax amount'), editable=False
    )
    total_tax = models.FloatField(
        verbose_name=_('Total tax amount'), editable=False
    )

    net_salary = models.FloatField(
        verbose_name=_('Net salary'), editable=False)

    contributions_other_total = models.FloatField(verbose_name=_('Other contributions total'))

    labour_cost = models.FloatField(
        verbose_name=_('Labour cost'), editable=False)

    def calculate_all(self, period_labour: List['Labour']) -> List['Payroll']:
        pass

    def save(self, *args, **kwargs):

        super(Payroll, self).save()

    def __str__(self):
        return f"""{self.date_of_accounting}"""
