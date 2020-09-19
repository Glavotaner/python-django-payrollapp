from django.db import models

from django.contrib import admin

from abstract.models import Person, Address 
from third_party.bank.models import Bank
from employee_data.employment.models import SignedContract
from calc_data.models import ContributionsModality, TaxModel

    
class Dependent(Person):
    
    
    child = models.BooleanField(default = False, verbose_name='Child')
    
    # FOREIGN KEYS
    dependent_of = models.ForeignKey('Employee', on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}
    Disability: {self.disability}
    Age: {self.age}
    Child: {self.child}"""
    


class Employee(Person, Address):

    
    # PROPERTIES
    ## DEPENDENTS
    @property
    def no_children(self):
        dep_counter = 0
        
        for dependent in Dependent.objects.filter(dependent_of = self.pid).all():
            if dependent.age <= 16:
                dep_counter += 1
        
        return dep_counter
    
    @property
    def no_dependents(self):
        dep_counter = 0
        
        for dependent in Dependent.objects.filter(dependent_of = self.pid).all():
            if dependent.age > 16:
                dep_counter += 1
        
        return dep_counter
    
    @property
    def no_dependents_disabled(self):
        dep_counter = 0
        
        for dependent in Dependent.objects.filter(dependent_of = self.pid).all():
            if dependent.disability == 'D':
                dep_counter += 1
        
        return dep_counter
    
    @property
    def no_dependents_disabled_100(self):
        dep_counter = 0
        
        for dependent in Dependent.objects.filter(dependent_of = self.pid).all():
            if dependent.disability == 'D100':
                dep_counter += 1
        
        return dep_counter
    
    
    iban = models.IntegerField(unique=True, verbose_name='IBAN')
    
    first_employment = models.BooleanField(default=True, verbose_name='First employment')
    first_employment_with_company = models.BooleanField(default = True, verbose_name='First employment with company')
    employee_since = models.DateField(verbose_name='Employee since')

    

    # FOREIGN KEYS
    employee_bank = models.ForeignKey(to = Bank, verbose_name = 'Bank', on_delete=models.DO_NOTHING)
    contributions_model = models.ForeignKey(ContributionsModality, on_delete=models.DO_NOTHING)
    signed_contract = models.ForeignKey(to = SignedContract,verbose_name='Contract type', on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.pid
    

