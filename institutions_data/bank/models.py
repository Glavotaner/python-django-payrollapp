from django.db import models
from django.db.models.signals import pre_delete

from common.models import Address


class Bank(Address):
    
    business_id = models.IntegerField(primary_key=True, verbose_name='Business ID')
    bank_name = models.CharField(max_length = 10, verbose_name='Bank name')
    
    
    def __str__(self):
        return f"""{self.bank_name}, {self.city}"""
