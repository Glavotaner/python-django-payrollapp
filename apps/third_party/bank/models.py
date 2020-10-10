from django.db import models

from apps.employee_data.employee.models.address import Address
from django.core.exceptions import ValidationError
from apps.general_services.validators.id_validators import validate_bid, validate_pid


class Bank(Address):

    business_id = models.CharField(
        primary_key=True, verbose_name='Business ID', max_length=8)
    oib = models.CharField(max_length=11, verbose_name='OIB')
    bank_name = models.CharField(max_length=20, verbose_name='Bank name')

    def clean(self):
        # validate_bid(self.business_id)
        # validate_pid(self.oib)
        pass

    def __str__(self):
        return f"""{self.bank_name}, {self.city}"""
