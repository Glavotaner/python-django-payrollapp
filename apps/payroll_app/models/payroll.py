from django.db import models
from django.utils.translation import gettext_lazy as _

from .labour import Labour
from apps.employee_data_app.employee_app.models import Employee
from apps.calculation_data_app.models import Deductible, TaxModel

from apps.payroll_app.services.calculations import tax_calculation, contributions_calculation, deductibles_calculation, gross_salary_calculation, var_calculation


class Payroll(models.Model):
    
    class Meta:
        verbose_name = _('Payroll')
        verbose_name_plural = _('Payrolls')
        

    date_of_accounting = models.DateTimeField(
        auto_now=True, verbose_name=_('Date of accounting'), db_index=True)
    accounted_period_start = models.DateField(
        verbose_name=_('Accounted period start'))
    accounted_period_end = models.DateField(
        verbose_name=_('Accounted period end'))
    
    current_deductibles_model = models.ForeignKey(Deductible, on_delete=models.DO_NOTHING, editable=False)
    
    current_tax_model = models.ForeignKey(TaxModel, on_delete=models.DO_NOTHING, editable=False)

    accounted_period_id = models.CharField(verbose_name=_(
        'Accounted period ID'), editable=False, max_length=15, unique=True)

    months_hours_fund = models.IntegerField(
        verbose_name=_("Month's hours fund"), editable=False, primary_key=True)
    

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

    contributions_base = models.FloatField(
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


    def save(self):
        
        self.current_deductibles_model = Deductible.objects.latest()
        
        self.current_tax_model = TaxModel.objects.latest()
        
        self.accounted_period_id = var_calculation._accounted_period_id(self)

        self.months_hours_fund = var_calculation._months_hours_fund(self)

        self.wage = gross_salary_calculation._wage(self)

        self.overtime_hours_gross = gross_salary_calculation._overtime_hours_gross(self)
        self.special_hours_gross = gross_salary_calculation._special_hours_gross(self)

        self.gross_salary = gross_salary_calculation._gross_salary(self)

        self.contributions_base = contributions_calculation._contributions_base(self)

        self.health_insurance_amount = contributions_calculation._health_insurance_amount(self)

        self.pension_fund_gen_amount = contributions_calculation._pension_fund_gen_amount(self)
        self.pension_fund_ind_amount = contributions_calculation._pension_fund_ind_amount(self)
        self.pension_fund_total = contributions_calculation._pension_fund_total(self)

        self.income = tax_calculation._income(self)

        self.personal_deductible_amount = deductibles_calculation._personal_deductible_amount(self)
        self.deductible_dependents = deductibles_calculation._deductible_dependents(self)
        self.deductible_children = deductibles_calculation._deductible_children(self)
        self.deductible_dependents_disabled = deductibles_calculation._deductible_dependents_disabled(
            self)
        self.deductible_dependents_disabled_100 = deductibles_calculation._deductible_dependents_disabled_100(
            self)
        self.total_deductibles = deductibles_calculation._total_deductibles(self)

        self.tax_base = tax_calculation._tax_base(self)

        self.income_tax_amount = tax_calculation._income_tax_amount(self)
        self.city_tax_amount = tax_calculation._city_tax_amount(self)
        self.total_tax = tax_calculation._total_tax(self)

        self.net_salary = tax_calculation._net_salary(self)

        self.labour_cost = tax_calculation._labour_cost(self)

        super(Payroll, self).save()
        

    def __str__(self):
        return f"""{self.accounted_period_id} | {self.current_deductibles_model} | {self.current_tax_model}"""
