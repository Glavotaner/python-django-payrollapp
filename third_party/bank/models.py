from django.db import models

from abstract.models import Address
from django.core.exceptions import ValidationError
import re


class Bank(Address):
    
    business_id = models.CharField(primary_key=True, verbose_name='Business ID', max_length=8)
    oib = models.CharField(max_length=11, verbose_name = 'OIB')
    bank_name = models.CharField(max_length = 10, verbose_name='Bank name')
    
    def clean(self):
        
        # BUSINESS ID VALIDATION
        if len(self.business_id) != 8:
            raise ValidationError('Business ID number is of an invalid length')
        if re.search('[^0-9]', self.business_id):
            raise ValidationError('Businnes ID number is not entirely numeric')
        
        control = int(self.business_id[-1])
    
        _bid = self.business_id[:-1]
        
        res = 0
        i = 8
        while i >= 2:
            res += (int(_bid[8-i]) * i)
            
            i -= 1
        
        res %= 11

        res = 11 - res
    
        if not res == 1 and control == 0 or 1 < res < 11 and control == res:
            raise ValidationError('Business ID number is invalid')

        
        #OIB VALIDATION
        if len(self.oib) != 11:
            raise ValidationError('OIB is of an invalid length')
        if re.search('[^0-9]', self.oib):
            raise ValidationError('OIB is not entirely numeric')
         
        control = self.oib[-1]
        previous_remainder = 0
        
        for i, num in enumerate(str(self.oib)):
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
            raise ValidationError('OIB is invalid, please check your input')

    
    def __str__(self):
        return f"""{self.bank_name}, {self.city}"""
