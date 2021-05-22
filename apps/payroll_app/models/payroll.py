from apps.calculation_data_app.models.tax_model import TaxModel
from apps.calculation_data_app.services.tax_calculation import TaxCalculated
from apps.calculation_data_app.models.deductibles_model import DeductiblesModel
from apps.calculation_data_app.services.deductibles_calculation import DeductibleCalculated
from apps.calculation_data_app.services.contributions_calculation import ContributionsModelCalculated
from apps.payroll_app.models.wage_parameters import WageParameters
from apps.payroll_app.services.calculations.salary_calculation import SalaryCalculated
from datetime import date
from typing import List, Dict

from django.db import models
from django.db.models.aggregates import Max
from django.utils.translation import gettext_lazy as _

from apps.payroll_app.models import Labour, ReimbursementAmount
from apps.calculation_data_app.models import Contribution, Reimbursement


class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)

    acc_counter = models.IntegerField(verbose_name=_('Accounting counter'))

    date_of_accounting = models.DateField(
        verbose_name=_('Date of accounting'), db_index=True)

    work_data = models.OneToOneField(
        Labour, on_delete=models.PROTECT, db_index=True, verbose_name=_('Work data'))

    valid_contributions = models.ManyToManyField(
        Contribution, editable=False, verbose_name=_('Valid contributions'))

    wage = models.FloatField(verbose_name=_('Wage'))

    gross_salary = models.FloatField(verbose_name=_('Gross salary'))

    contributions_base = models.FloatField(
        verbose_name=_('Contributions base'))

    contributions_frompay_total = models.FloatField(
        verbose_name=_('Total contributions from pay'))
    contributions_other_total = models.FloatField(
        verbose_name=_('Other contributions total'))

    income = models.FloatField(verbose_name=_('Income'))

    personal_deductible_amount = models.FloatField(
        verbose_name=_('Personal deductible amount'))
    deductible_dependents = models.FloatField(
        verbose_name=_('Dependents deductible amount'))
    deductible_children = models.FloatField(
        verbose_name=_('Children deductible amount'))
    deductible_dependents_disabled = models.FloatField(
        verbose_name=_('Disabled dependents deductible amount'))
    deductible_dependents_disabled_100 = models.FloatField(
        verbose_name=_('100% disabled dependents deductible amount'))
    total_deductibles = models.FloatField(
        verbose_name=_('Total deductibles amount'))

    tax_base = models.FloatField(verbose_name=_('Tax base'))

    income_tax_amount = models.FloatField(verbose_name=_('Income tax amount'))
    city_tax_amount = models.FloatField(verbose_name=_('City tax amount'))
    total_tax = models.FloatField(verbose_name=_('Total tax amount'))

    net_salary = models.FloatField(verbose_name=_('Net salary'))

    reimbursements_total = models.FloatField(
        verbose_name=_('Reimbursements total'), null=True, blank=True)

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
    def calculate_reimbursements(
            accounting_date: date,
            reimbursements: List[Dict],
            payrolls: List['Payroll'] = None
    ) -> None:
        if not payrolls:
            payrolls = Payroll.objects.filter(accounting_date=accounting_date)
        payrolls_to_update: List['Payroll'] = []
        reimbursements_to_save: List = []
        reimbursements_total: float = 0

        for payroll in payrolls:
            for reimbursement in reimbursements:
                reimbursements_total += reimbursement['amount']
                reimbursements_to_save.append(ReimbursementAmount.objects.create(
                    reimbursement=Reimbursement.objects.get(reimbursement['id']),
                    amount=reimbursement['amount'],
                    payroll=payroll
                ))

            payroll.reimbursements_total = reimbursements_total
            payroll.net_salary += reimbursements_total
            payrolls_to_update.append(payroll)

        ReimbursementAmount.objects.bulk_create(reimbursements_to_save)
        Payroll.objects.bulk_update(payrolls_to_update, ['reimbursements_total', 'net_salary'])

    @staticmethod
    def calculate_payrolls(
            accounting_date: date,
            year: int, month: int,
            labours: List['Labour'] = None
    ) -> None:
        current_wage_parameters: WageParameters = \
            WageParameters.get_valid_wage_parameters(accounting_date)

        labour_to_calculate: List[Labour] = []

        if not labours:
            labours = Labour.objects.filter(year=year, month=month)
        for labour in labours:
            salary_calculated: SalaryCalculated = SalaryCalculated(
                labour, accounting_date, current_wage_parameters
            )
            wage: float = salary_calculated.wage_real
            gross_salary: float = salary_calculated.total_salary
            contributions_calculated: ContributionsModelCalculated = \
                ContributionsModelCalculated(
                    current_wage_parameters,
                    labour.employee.contributions_model,
                    labour,
                    salary_calculated.contributions_base
                )
            contributions_from_pay: float = \
                contributions_calculated.calculated_contributions_from_pay
            contributions_other: float = \
                contributions_calculated.calculated_contributions_other
            income: float = gross_salary - contributions_from_pay
            deductibles_calculated: DeductibleCalculated = DeductibleCalculated(
                DeductiblesModel.get_valid_deductibles_model(accounting_date),
                labour
            )
            tax_base: float = income - deductibles_calculated.total_deductible
            tax_base = tax_base if tax_base > 0 else 0
            tax_calculated: TaxCalculated = TaxCalculated(
                TaxModel.get_valid_tax_model(accounting_date),
                tax_base,
                labour.employee.city.tax_rate,
                labour.employee.hrvi,
                labour.employee.tax_breaks
            )

            labour_to_calculate.append(Payroll.objects.create(
                acc_counter=Payroll.get_accounting_counter_for_period(
                    year, month
                ),
                date_of_accounting=accounting_date,
                work_data=labour,
                valid_contributions=Contribution.get_current_contributions(),

                wage=wage,
                gross_salary=gross_salary,

                contributions_base=salary_calculated.contributions_base,
                contributions_frompay_total=contributions_from_pay,
                contributions_other_total=contributions_other,

                income=income,

                personal_deductible_amount=deductibles_calculated.personal_deductible,
                deductible_dependents=deductibles_calculated.adults_deductible,
                deductible_children=deductibles_calculated.children_deductible,
                deductible_dependents_disabled=deductibles_calculated.disabled_deductible,
                deductible_dependents_disabled_100=deductibles_calculated.disabled_100_deductible,
                total_deductibles=deductibles_calculated.total_deductible,

                tax_base=tax_base,
                income_tax_amount=tax_calculated.income_tax,
                city_tax_amount=tax_calculated.city_tax,
                total_tax=tax_calculated.total_tax,

                net_salary=income - tax_calculated.total_tax,
                labour_cost=gross_salary + contributions_other
            ))
        Payroll.objects.bulk_create(labour_to_calculate)

    @staticmethod
    def get_accounting_counter_for_period(year: int, month: int) -> int:
        if Payroll.objects.filter(year=year, month=month).count() > 0:
            return Payroll.objects.filter(year=year, month=month).aggregate(Max('acc_counter'))['acc_counter__max'] + 1
        return 1
