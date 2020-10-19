from django.db import models
from django.utils.translation import gettext_lazy as _

from .labour import Labour
from apps.employee_data_app.employee_app.models import Employee
from apps.calculation_data_app.models import HourFund, Deductible, TaxModel

from apps.payroll_app.services.calculations import tax_calculation, contributions_calculation, deductibles_calculation, gross_salary_calculation, var_calculation


class Payroll(models.Model):
    

    date_of_accounting = models.DateTimeField(
        auto_now=True, verbose_name=_('Date of accounting'), db_index=True)
    accounted_period_start = models.DateField(
        verbose_name=_('Accounted period start'))
    accounted_period_end = models.DateField(
        verbose_name=_('Accounted period end'))
    accounted_period_id = models.CharField(verbose_name=_(
        'Accounted period ID'), editable=False, max_length=15, unique=True)

    months_hours_fund = models.IntegerField(
        verbose_name=_("Month's hours fund"), editable=False)

    @property
    def current_deductibles_model(self):
        return Deductible.objects.latest()

    @property
    def current_tax_model(self):
        return TaxModel.objects.latest()


    employee = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, db_index=True, verbose_name=_('Employee'))
    work_data = models.OneToOneField(
        Labour, on_delete=models.DO_NOTHING, db_index=True, verbose_name=_('Work data'))

    wage = models.FloatField(verbose_name=_('Wage'), editable=False)
    overtime_hours_gross = models.FloatField(
        verbose_name=_('Overtime hours gross'), editable=False)
    special_hours_gross = models.FloatField(
        verbose_name=_('Special hours gross'), editable=False)
    gross_salary = models.FloatField(
        verbose_name=_('Gross salary'), editable=False)

    contributons_base = models.FloatField(
        verbose_name=_('Contributions base'), editable=False)

    health_insurance_amount = models.FloatField(
        verbose_name=_('Health insurance amount'), editable=False)

    pension_fund_gen_amount = models.FloatField(verbose_name=_(
        'Generational pension fund contribution amount'), editable=False)
    pension_fund_ind_amount = models.FloatField(
        verbose_name=_('Individual pension fund amount'), editable=False)
    pension_fund_total = models.FloatField(verbose_name=_(
        'Total pension fund contribution amount'), editable=False)

    income = models.FloatField(verbose_name=_('Income'), editable=False)

    personal_deductible_amount = models.FloatField(
        verbose_name=_('Personal deductible amount'), editable=False)

    deductible_dependents = models.FloatField(
        verbose_name=_('Dependents deductible amount'), editable=False)
    deductible_children = models.FloatField(
        verbose_name=_('Children deductible amount'), editable=False)
    deductible_dependents_disabled = models.FloatField(
        verbose_name=_('Disabled dependents deductible amount'), editable=False)
    deductible_dependents_disabled_100 = models.FloatField(verbose_name=_(
        '100% disabled dependents deductible amount'), editable=False)
    total_deductibles = models.FloatField(
        verbose_name=_('Total deductibles amount'), editable=False)

    tax_base = models.FloatField(verbose_name=_('Tax base'), editable=False)
    income_tax_amount = models.FloatField(
        verbose_name=_('Income tax amount'), editable=False)
    city_tax_amount = models.FloatField(
        verbose_name=_('City tax amount'), editable=False)
    total_tax = models.FloatField(
        verbose_name=_('Total tax amount'), editable=False)

    net_salary = models.FloatField(
        verbose_name=_('Net salary'), editable=False)

    labour_cost = models.FloatField(
        verbose_name=_('Labour cost'), editable=False)
    
    class Meta:
        verbose_name = _('Payroll')
        verbose_name_plural = _('Payrolls')

    def __str__(self):
        return f"""{self.accounted_period} | {self.current_deductibles_model} | {self.current_tax_model}"""