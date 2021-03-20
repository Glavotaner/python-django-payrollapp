from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Address


class Bank(Address):
    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Banks')

    business_id = models.CharField(
        verbose_name=_('Business ID'),
        max_length=8,
        help_text=_('Input valid business ID')
    )

    oib = models.CharField(
        primary_key=True,
        max_length=11,
        verbose_name=_('OIB'),
        help_text=_('Input valid PID')
    )

    bank_name = models.CharField(max_length=40, verbose_name=_('Bank name'))

    iban = models.CharField(max_length=40, verbose_name=_('IBAN'))

    def clean(self):
        # validate_bid(self.business_id)
        # validate_pid(self.oib)
        pass

    def __str__(self):
        return f"""{self.bank_name}, {self.city}"""
