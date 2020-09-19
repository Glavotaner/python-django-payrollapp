from django.db import models

from abstract.models import Address


class Bank(Address):
    
    business_id = models.IntegerField(primary_key=True, verbose_name='Business ID')
    oib = models.CharField(max_length=11, verbose_name = 'OIB')
    bank_name = models.CharField(max_length = 10, verbose_name='Bank name')
    
    
    def __str__(self):
        return f"""{self.bank_name}, {self.city}"""
