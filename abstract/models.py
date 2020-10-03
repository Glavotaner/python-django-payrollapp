from django.db import models
from django.contrib import admin

import re
from datetime import timezone, date
from third_party.city.models import City
from django.core.exceptions import ValidationError



class AbstractAddress(models.Model):
    
    class Meta:
        abstract = True
    
    street_name = models.CharField(max_length = 20, verbose_name='Street name')
    street_number = models.IntegerField(verbose_name='Street number')
    city = models.ForeignKey(City, verbose_name='City name', on_delete=models.DO_NOTHING)
    
    phone_number = models.CharField(max_length = 15, verbose_name = 'Phone number')
    

class Address(AbstractAddress):
    
    class Meta:
        verbose_name_plural = "Addresses"
    
    def __str__(self):
        return f"""{self.street_name} {self.street_number}, {self.postal_code} {self.city}"""

   

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
        today = date.today() 
        try:  
            birthday = self.date_of_birth.replace(year = today.year) 
     
        except ValueError:  
            birthday = self.date_of_birth.replace(year = today.year, 
                    month = self.date_of_birth.month + 1, day = 1) 
    
        if birthday > today: 
            return today.year - self.date_of_birth.year - 1
        else: 
            return today.year - self.date_of_birth.year 
        
    disability = models.CharField(choices=disability, max_length=4, verbose_name='Disability', default = NONE)
    

class Person(PersonModel):
    
    def clean(self):
        
        #PID VALIDATION
        if len(self.pid) != 11:
            raise ValidationError('PID is of an invalid length')
        if re.search('[^0-9]', self.pid):
            raise ValidationError('PID is not entirely numeric')
         
        control = self.pid[-1]
        previous_remainder = 0
        
        for i, num in enumerate(str(self.pid)):
            num = int(num)    

            if i == 10:
                break
            
            if i == 0:
                num += 10
            else:
                num += previous_remainder
            
            if num % 10 == 0:
                num = 10
            else:
                num %= 10
                    
            num *= 2
            
            num %= 11

            previous_remainder = num

        if previous_remainder == 1:
            valid = ((11 - previous_remainder) % 10) == int(control)
        
        else:
            valid = (11 - previous_remainder) == int(control)
        
        if not valid:
            raise ValidationError('PID is invalid, please check your input')
        
        if self.age < 18:
            raise ValidationError('Employee cannot be underage')
            
        
    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}"""
    


    
    