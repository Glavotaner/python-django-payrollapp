from django.db import models
from .dependent import Dependent
from django.contrib import admin

from datetime import date
import re

from .person import Person
from .address import Address
from apps.third_parties_app.models import Bank
from apps.employee_data_app.employment_app.models import Contract
from apps.calculation_data_app.models import ContributionsModality, TaxModel
from django.core.exceptions import ValidationError
from apps.general_services.validators.id_validators import validate_iban
from apps.general_services.validators.person_validation import validate_age
from apps.employee_data_app.employee_app.services.dependents_calculator import *
    


class Employee(Person, Address):   

    
    # PROPERTIES
    ## DEPENDENTS
    @property
    def no_children(self):
        return calculate_no_children(self.pid)
    
    @property
    def no_dependents(self):
        return calculate_no_dependents(self.pid)
    
    @property
    def no_dependents_disabled(self):
        return caluclate_no_dependents_disabled(self.pid)
    
    @property
    def no_dependents_disabled_100(self):
        return calculate_no_dependents_disabled_100(self.pid)

        
    iban = models.CharField(unique=True, verbose_name='IBAN', max_length = 34)
    
    
    # FIRST EMPLOYMENT DATA
    first_employment = models.BooleanField(default=True, verbose_name='First employment')
    first_employment_with_company = models.BooleanField(default = True, verbose_name='First employment with company')
    
    employee_since = models.DateField(verbose_name='Employee since', auto_now = True)
    

    # FOREIGN KEYS
    employee_bank = models.ForeignKey(to = Bank, verbose_name = 'Bank', on_delete=models.DO_NOTHING)
    
    contributions_model = models.ForeignKey(ContributionsModality, on_delete=models.DO_NOTHING)
    
    signed_contract = models.ForeignKey(to = Contract,verbose_name='Contract', on_delete=models.DO_NOTHING)
    
    
    def clean(self):
        validate_age(self.date_of_birth)
        #validate_iban(self.iban)


    def __str__(self):
        return f"{self.pid}"
    

