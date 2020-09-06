from django.db import models
from django.db.models.signals import pre_delete

from common.models import BankAddress


class Bank(models.Model):
    
    business_id = models.IntegerField(primary_key=True, verbose_name='Business ID')
    bank_name = models.CharField(max_length = 10, verbose_name='Bank name')
    address = models.OneToOneField(BankAddress, on_delete = models.CASCADE)
    
    def delete_address(self, sender, **kwargs):
        return not self.address == None
    
    pre_delete.connect(delete_address, sender=BankAddress)
    
    def __str__(self):
        return f"""{self.bank_name}, {self.address}"""
