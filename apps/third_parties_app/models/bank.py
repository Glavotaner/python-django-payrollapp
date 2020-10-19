from django.db import models

from apps.employee_data_app.employee_app.models import Address
from django.core.exceptions import ValidationError
from apps.general_services.validators.id_validators import validate_bid, validate_pid
from django.utils.translation import gettext_lazy as _


class Bank(Address):

    business_id = models.CharField(
        primary_key=True, verbose_name=_('Business ID'), max_length=8, help_text = _('Input valid business ID'))
    oib = models.CharField(max_length=11, verbose_name='OIB', help_text = _('Input valid OID ID'))
    bank_name = models.CharField(max_length=20, verbose_name=_('Bank name'))

    def clean(self):
        # validate_bid(self.business_id)
        # validate_pid(self.oib)
        pass

    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Banks')

    def __str__(self):
        return f"""{self.bank_name}, {self.city}"""
