from datetime import date
from typing import List, Dict

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.payroll_app.models import Labour
from apps.calculation_data_app.models import Contribution


class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)

    acc_counter = models.IntegerField(verbose_name=_('Accounting counter'))

    date_of_accounting = models.DateField(verbose_name=_('Date of accounting'), db_index=True)

    work_data = models.OneToOneField(Labour, on_delete=models.PROTECT, db_index=True, verbose_name=_('Work data'))

    valid_contributions = models.ManyToManyField(Contribution, editable=False, verbose_name=_('Valid contributions'))

    wage = models.FloatField(verbose_name=_('Wage'))

    gross_salary = models.FloatField(verbose_name=_('Gross salary'))

    contributions_base = models.FloatField(verbose_name=_('Contributions base'))

    contributions_frompay_total = models.FloatField(verbose_name=_('Total contributions from pay'))
    contributions_other_total = models.FloatField(verbose_name=_('Other contributions total'))

    income = models.FloatField(verbose_name=_('Income'))

    personal_deductible_amount = models.FloatField(verbose_name=_('Personal deductible amount'))
    deductible_dependents = models.FloatField(verbose_name=_('Dependents deductible amount'))
    deductible_children = models.FloatField(verbose_name=_('Children deductible amount'))
    deductible_dependents_disabled = models.FloatField(verbose_name=_('Disabled dependents deductible amount'))
    deductible_dependents_disabled_100 = models.FloatField(verbose_name=_('100% disabled dependents deductible amount'))
    total_deductibles = models.FloatField(verbose_name=_('Total deductibles amount'))

    tax_base = models.FloatField(verbose_name=_('Tax base'))

    income_tax_amount = models.FloatField(verbose_name=_('Income tax amount'))
    city_tax_amount = models.FloatField(verbose_name=_('City tax amount'))
    total_tax = models.FloatField(verbose_name=_('Total tax amount'))

    net_salary = models.FloatField(verbose_name=_('Net salary'))

    reimbursements_total = models.FloatField(verbose_name=_('Reimbursements total'))

    labour_cost = models.FloatField(verbose_name=_('Labour cost'))

    class Meta:
        verbose_name = _('Payroll')
        verbose_name_plural = _('Payrolls')

        db_table = 'payrolls'

    def __str__(self):
        return f"""{self.date_of_accounting}"""

    def save(self, *args, **kwargs):
        super(Payroll, self).save()

    @staticmethod
    def calculate_all(accounting_date: date, year: int, month: int,
                      labour: List['Labour'] = None, reimbursement_amounts: List[Dict] = None) -> None:
        if not labour:
            labour = Labour.objects.filter(year=year, month=month)
