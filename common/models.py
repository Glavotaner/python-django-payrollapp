from django.db import models

import datetime 
from dateutil.relativedelta import relativedelta

# Create your models here.


class Address(models.Model):
    
    class Meta:
        abstract = True
    
    street_name = models.CharField(max_length = 20, verbose_name='Street name')
    street_number = models.IntegerField(verbose_name='Street number')
    postal_code = models.IntegerField(verbose_name='Postal code')
    city = models.CharField(max_length = 20, verbose_name='City')
    

class PersonalAddress(Address):
    
    class Meta:
        verbose_name_plural = "Personal Addresses"
    
    def __str__(self):
        return f"""{self.street_name} {self.street_number}, {self.postal_code} {self.city}"""


class BankAddress(Address):
    
    class Meta:
        verbose_name_plural = "Bank Addresses"
    
    def __str__(self):
        return f"""{self.city}"""
    

class PersonModel(models.Model):
    
    class Meta:
        abstract = True
        
    
    DISABLED = 'D'
    DISABLED_100 = 'D100'
    NONE = 'N'
    
    disability = [
        (DISABLED, 'Disabled'),
        (DISABLED_100, '100% disabled'),
        (NONE, 'None')
    ]
    
    pid = models.CharField(primary_key = True, max_length = 11, verbose_name='PID')
    first_name = models.CharField(max_length = 30, verbose_name='First name')
    last_name = models.CharField(max_length = 20, verbose_name='Last name')
    date_of_birth = models.DateField(verbose_name='Date of birth')
    
    @property
    def age(self):
       
        return 10
    
    address = models.ForeignKey(PersonalAddress, on_delete=models.CASCADE)
    
    disability = models.CharField(choices=disability, max_length=4, verbose_name='Disability', default = NONE)
    
    
class Person(PersonModel):
    
    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}"""
    