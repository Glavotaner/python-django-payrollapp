from django.db import models

from employee_data.employee.models import Employee
from calc_data.models import HourFund, Deductible, TaxModel

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
    
    @property
    def current_deductibles_model(self):
        return Deductible.objects.latest()
    
    @property
    def current_tax_model(self):
        return TaxModel.objects.latest()
    
    @property
    def accounted_period(self):
        return f"From {self.accounted_period_start} to {self.accounted_period_end}"
    
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    work_data = models.OneToOneField(Labour, on_delete=models.DO_NOTHING)
    
    
    @property
    def months_hours_fund(self):
       
        acc_period_year = str(self.accounted_period_start)[0:4]
        acc_period_month = str(self.accounted_period_start)[5:7]
        
        monthly_hours_fund_id = HourFund.objects.get(year = acc_period_year, month = acc_period_month)
        
        return monthly_hours_fund_id.total_hours


    @property
    def wage(self):
        return round(float(self.employee.signed_contract.position.salary) / self.months_hours_fund, 2)


    ## HOURS GROSS
    
    @property
    def overtime_hours_gross(self):
        return round(self.work_data.overtime_hours * self.wage + (self.wage * 0.33), 2)
    
    @property
    def special_hours_gross(self):
        return round(self.work_data.special_hours * self.wage + (self.wage * 0.25), 2)
    
    
    ## GROSS SALARY
    
    @property
    def gross_salary(self):
        
        if self.work_data.regular_hours < self.months_hours_fund:
            return self.wage * self.work_data.regular_hours
        
        return round(self.employee.signed_contract.position.salary, 2)
    
    
    ## CONTRIBUTIONS
    
    @property
    def health_insurance_amount(self):
        return round(self.gross_salary * self.employee.contributions_model.health_insurance, 2)
    
    @property
    def pension_fund_gen_amount(self):
        return round(self.gross_salary * self.employee.contributions_model.pension_fund_gen, 2)
    
    @property
    def pension_fund_ind_amount(self):
        return round(self.gross_salary * self.employee.contributions_model.pension_fund_ind, 2)
    
    @property
    def pension_fund_total(self):
        return round(self.pension_fund_gen_amount + self.pension_fund_ind_amount, 2)
    
    
    @property
    def income(self):
        if self.gross_salary - self.pension_fund_total < self.employee.contributions_model.pension_fund_min_base:
            return self.employee.contributions_model.pension_fund_min_base
        
        return self.gross_salary - self.pension_fund_total
    
    
    ## DEDUCTIBLES
    
    @property
    def personal_deductible_amount(self):
        return self.current_deductibles_model.base_deductible * self.current_deductibles_model.personal_deductible_coef
    
    
    @property
    def dependents_children(self):
        child_coefs = [0.7, 1.0, 1.4, 1.9, 2.5, 3.2, 4.0, 4.9, 5.9, 7]
        
        if 0 < self.employee.no_children < 10:
            return child_coefs[self.employee.no_children - 1] * self.current_deductibles_model.base_deductible
        elif self.employee.no_children <= 0:
            return 0
        else:
            return ((self.employee.no_children - 9) * 1.1 + 7) * self.current_deductibles_model.base_deductible
    
    @property
    def dependents_deductible(self):
        return self.employee.no_dependents * 0.7 * self.current_deductibles_model.base_deductible
    
    @property
    def disabled_dependents(self):
        return self.employee.no_dependents_disabled * 0.4 * self.current_deductibles_model.base_deductible
    
    @property
    def disabled_dependents_100(self):
        return self.employee.no_dependents_disabled_100 * 0.5 * self.current_deductibles_model.base_deductible
    
    @property
    def deductibles(self):
        return self.personal_deductible_amount + self.dependents_children + self.dependents_deductible + self.disabled_dependents + self.disabled_dependents_100
   
   
    @property 
    def tax_base(self):
        
        
        if self.deductibles > self.income:
            return 0
        
        return self.income - self.deductibles
    
    
    # TAX    
    @property
    def income_tax_amount(self):
        
        if self.employee.age <= 25:
            return 0
        
        if self.tax_base > self.current_tax_model.tax_bracket:
            hi_tax_base = self.tax_base - self.current_tax_model.tax_bracket
            
            income_tax = (self.current_tax_model.tax_bracket * self.current_tax_model.lo_tax_rate) + (hi_tax_base * self.current_tax_model.hi_tax_rate) 
        
        else:
            income_tax = self.tax_base * self.current_tax_model.lo_tax_rate
            
        if 25 > self.employee.age <= 30:
            return income_tax / 2
             
        return income_tax
    
    @property
    def city_tax_amount(self):
        return self.income_tax_amount * (self.employee.city.tax_rate - self.employee.city.tax_break)
    
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
        return f"""{self.accounted_period} | {self.current_deductibles_model} | {self.current_tax_model}"""
    
    
    
