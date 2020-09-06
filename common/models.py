from django.db import models

import datetime 
from dateutil.relativedelta import relativedelta

# Create your models here.


class Address(models.Model):
    
    class Meta:
        abstract = True
    
    street_name = models.CharField(max_length = 20)
    street_number = models.IntegerField()
    postal_code = models.IntegerField()
    city = models.CharField(max_length = 20)
    

class PersonalAddress(Address):
    
    def __str__(self):
        return f"""{self.street_name} {self.street_number}, {self.postal_code} {self.city}"""


class BankAddress(Address):
    
    def __str__(self):
        return f"""{self.city}"""
    

class PersonModel(models.Model):
    
    DISABLED = 'D'
    DISABLED_100 = 'D100'
    
    disability = [
        (DISABLED, 'Disabled'),
        (DISABLED_100, '100% disabled')
    ]
    
    pid = models.CharField(primary_key = True, max_length = 11)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 20)
    date_of_birth = models.DateField()
    
    @property
    def age(self):
       
        return 10
    
    address = models.ForeignKey(PersonalAddress, on_delete=models.CASCADE)
    
    disability = models.CharField(choices=disability, max_length=4)
    
    
class Person(PersonModel):
    
    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}"""
    