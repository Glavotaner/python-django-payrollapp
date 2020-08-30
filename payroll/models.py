from django.db import models

from bank.models import Bank
from employee.models import Employee, PaymentInfo
 
class Labour(models.Model):
    
    employee = models.OneToOneField(Employee, on_delete=models.DO_NOTHING)
    labour_period = models.DateField()
    regular_hours = models.IntegerField()
    overtime_hours = models.IntegerField()
    holiday_hours = models.IntegerField()
    sunday_hours = models.IntegerField()
    

class Payroll(models.Model):
    
    date_of_accounting = models.DateTimeField(auto_now=True)
    accounted_period = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.DO_NOTHING)
    work_data = models.OneToOneField(Labour, on_delete=models.DO_NOTHING)
    wage = models.IntegerField()
    
    # HOURS GROSS
    @property
    def regular_hours_gross(self):
        return self.work_data.regular_hours * self.wage
    
    @property
    def overtime_hours_gross(self):
        return self.work_data.overtime_hours * self.wage + (self.wage * 0.25)
    
    @property
    def holiday_hours_gross(self):
        return self.work_data.holiday_hours * self.wage + (self.wage * 0.25)
    
    @property
    def sunday_hours_gross(self):
        return self.work_data.sunday_hours * self.wage + (self.wage * 0.25)
    
    
    # GROSS SALARY
    @property
    def gross_salary(self):
        return self.regular_hours_gross + self.overtime_hours_gross + self.holiday_hours_gross + self.sunday_hours_gross
    
    @property
    def health_insurance_amount(self):
        return self.gross_salary * 0.165
    
    @property
    def income(self):
        return self.gross_salary - (self.gross_salary * 0.15 + self.gross_salary * 0.05)
    
    @property 
    def tax_base(self):
        if self.income - 4000 > 0:
            return self.income - 4000 
        else:
            return 0
    
    @property
    def tax_amount(self):
        income_tax = self.tax_base * 0.24
        city_tax = income_tax * 0.13
        
        return income_tax + city_tax
    
    # NET SALARY
    @property
    def net_salary(self):
        return self.income - self.tax_amount
    
    # LABOUR COST
    @property
    def labour_cost(self):
        return self.gross_salary + self.health_insurance_amount
    
    def __str__(self):
        return f"""Net salary: {self.net_salary}
    Labour cost: {self.labour_cost}"""
    
    
    
    
