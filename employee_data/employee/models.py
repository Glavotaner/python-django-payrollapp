from django.db import models

from django.contrib import admin

from datetime import date
import re

from abstract.models import Person, Address 
from third_party.bank.models import Bank
from employee_data.employment.models import Contract
from calc_data.models import ContributionsModality, TaxModel
from django.core.exceptions import ValidationError

    
class Dependent(Person):
    
    
    child = models.BooleanField(default = False, verbose_name='Child')
    
    # FOREIGN KEYS
    dependent_of = models.ForeignKey('Employee', on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.pid}"
    


class Employee(Person, Address):
    
    def clean(self):
        
        today = date.today() 
        try:  
            birthday = self.date_of_birth.replace(year = today.year) 
    
        # raised when birth date is February 29 
        # and the current year is not a leap year 
        except ValueError:  
            birthday = self.date_of_birth.replace(year = today.year, 
                    month = self.date_of_birth.month + 1, day = 1) 
    
        if birthday > today: 
            _age = today.year - self.date_of_birth.year - 1
        else: 
            _age = today.year - self.date_of_birth.year
        
        if _age < 18:
            raise ValidationError('Employee cannot be underage')
        
        # CHECK _IBAN
        
        valid = False
        
        _country2length = dict(
    AL=28, AD=24, AT=20, AZ=28, BE=16, BH=22, BA=20, BR=29,
    BG=22, CR=21, HR=21, CY=28, CZ=24, DK=18, DO=28, EE=20,
    FO=18, FI=18, FR=27, GE=22, DE=22, GI=23, GR=27, GL=18,
    GT=28, HU=28, IS=26, IE=22, IL=23, IT=27, KZ=20, KW=30,
    LV=21, LB=28, LI=21, LT=20, LU=20, MK=19, MT=31, MR=27,
    MU=30, MC=27, MD=24, ME=22, NL=18, NO=15, PK=24, PS=29,
    PL=28, PT=25, RO=24, SM=27, SA=24, RS=22, SK=24, SI=19,
    ES=24, SE=24, CH=21, TN=24, TR=26, AE=23, GB=22, VG=24 )
 
        # Ensure upper alphanumeric input.
        _iban = self.iban.replace(' ','').replace('\t','')
        if not re.match(r'^[\dA-Z]+$', _iban): 
            raise ValidationError('_IBAN is not alphanumeric input')
        # Validate country code against expected length.
        if len(_iban) != _country2length[_iban[:2]]:
            raise ValidationError('_IBAN country code is not a correct length')
        # Shift and convert.
        _iban = _iban[4:] + _iban[:4]
        digits = int(''.join(str(int(ch, 36)) for ch in _iban)) #BASE 36: 0..9,A..Z -> 0..35
        if not digits % 97 == 1:
            raise ValidationError('IBAN is invalid')

    
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
            if dependent.child:
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

        
    iban = models.CharField(unique=True, verbose_name='IBAN', max_length = 34)
    
    
    # FIRST EMPLOYMENT DATA
    first_employment = models.BooleanField(default=True, verbose_name='First employment')
    first_employment_with_company = models.BooleanField(default = True, verbose_name='First employment with company')
    
    employee_since = models.DateField(verbose_name='Employee since', auto_now = True)
    

    # FOREIGN KEYS
    employee_bank = models.ForeignKey(to = Bank, verbose_name = 'Bank', on_delete=models.DO_NOTHING)
    contributions_model = models.ForeignKey(ContributionsModality, on_delete=models.DO_NOTHING)
    signed_contract = models.ForeignKey(to = Contract,verbose_name='Contract', on_delete=models.DO_NOTHING)


    def __str__(self):
        return f"{self.pid}"
    

