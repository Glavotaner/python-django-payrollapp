from django.db import models

from employee_data.employee.models import Employee

"""
TODOS:

- Auto labour period charfield

CALCS:
- base case
- min wage
- income < deductible
- contribution modalities
- tax breaks
- less than full hours
-- proportional contr base, salary
 

"""
 
class Labour(models.Model):
    
    class Meta:
        verbose_name_plural = "Labour data"
        
    
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    labour_period = models.DateField(verbose_name='Labour period')
    labour_start_date = models.DateField(verbose_name = 'Labour start date')
    labour_end_date = models.DateField(verbose_name = 'Labour end date')
    regular_hours = models.IntegerField(verbose_name='Regular hours')
    overtime_hours = models.IntegerField(verbose_name='Overtime hours')
    special_hours = models.IntegerField(verbose_name='Holiday hours')
    
    def __str__(self):
        return f"""Employee ID: {self.employee.pid}
    Regular hours: {self.regular_hours}
    Overtime hours: {self.overtime_hours}
    Special hours: {self.special_hours}"""
    
    

class Payroll(models.Model):
    
    
    date_of_accounting = models.DateTimeField(auto_now=True, verbose_name='Date of accounting')
    accounted_period_start = models.DateField(verbose_name='Accounted period start')
    accounted_period_end = models.DateField(verbose_name = 'Accounted period end')
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    work_data = models.OneToOneField(Labour, on_delete=models.DO_NOTHING)
    
    @property
    def accounted_period(self):
        return f"From {self.accounted_period_start} to {self.accounter_period_end}"
    
    @property
    def wage(self):
        return self.employee.signed_contract.position.salary
    
    BASE_DEDUCTIBLE = 2500
    PERSONAL_DEDUCTIBLE = BASE_DEDUCTIBLE * 1.4
    
    # HOURS GROSS
    @property
    def regular_hours_gross(self):
        return self.work_data.regular_hours * self.wage
    
    @property
    def overtime_hours_gross(self):
        return self.work_data.overtime_hours * self.wage + (self.wage * 0.33)
    
    @property
    def special_hours_gross(self):
        return self.work_data.special_hours * self.wage + (self.wage * 0.25)
    
    
    # GROSS SALARY
    @property
    def gross_salary(self):
        return self.regular_hours_gross + self.overtime_hours_gross +  self.special_hours_gross
    
    
    # CONTRIBUTIONS
    @property
    def health_insurance_amount(self):
        return self.gross_salary * 0.165
    
    @property
    def pension_fund_one(self):
        return self.gross_salary * 0.15
    
    @property
    def pension_fund_two(self):
        return self.gross_salary * 0.05
    
    
    @property
    def income(self):
        return self.gross_salary - (self.pension_fund_one + self.pension_fund_two)
    
    
    # DEDUCTIBLES
    @property
    def dependents_children(self):
        child_coefs = [0.7, 1.0, 1.4, 1.9, 2.5, 3.2, 4.0, 4.9, 5.9, 7]
        
        if 0 < self.employee.no_children < 10:
            return child_coefs[self.employee.no_children - 1] * 2500
        elif self.employee.no_children <= 0:
            return 0
        else:
            return ((self.employee.no_children - 9) * 1.1 + 7) * 2500
    
    @property
    def dependents_deductible(self):
        return self.employee.no_dependents * 1750
    
    @property
    def disabled_dependents(self):
        return self.employee.no_dependents_disabled * 1000
    
    @property
    def disabled_dependents_100(self):
        return self.employee.no_dependents_disabled_100 * 3750
    
    @property
    def deductibles(self):
        return self.PERSONAL_DEDUCTIBLE + self.dependents_children + self.dependents_deductible + self.disabled_dependents + self.disabled_dependents_100
   
   
    @property 
    def tax_base(self):
        _tax_base = self.income - self.deductibles
        
        if _tax_base < 0:
            return 0
        else:
            return _tax_base
    
    
    # TAX    
    @property
    def income_tax_amount(self):
        if self.tax_base <= 30000:
            return self.tax_base * 0.24
        else:
            return self.tax_base * 0.36
    
    @property
    def city_tax_amount(self):
        return self.income_tax_amount * 0.13
    
    @property
    def tax_amount(self):
        return self.income_tax_amount + self.city_tax_amount
    
    
    
    # NET SALARY
    @property
    def net_salary(self):
        return self.income - self.tax_amount
    
    # LABOUR COST
    @property
    def labour_cost(self):
        return self.gross_salary + self.health_insurance_amount
    
    
    def __str__(self):
        return f"""{self.accounted_period}"""    
    
    
