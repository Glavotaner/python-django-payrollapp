from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Address


class Bank(Address):

    bank_id = models.AutoField(primary_key=True)

    oib = models.CharField(
        max_length=11,
        verbose_name=_('PID'),
        help_text=_('Input valid PID'),
        unique=True
    )

    bank_name = models.CharField(max_length=100, verbose_name=_('Bank name'))
    iban = models.CharField(max_length=22, verbose_name='IBAN')

    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Banks')

        db_table = 'banks'

    def __str__(self):
        return f"""{self.bank_name}, {self.city}"""

    def clean(self):
        # validate_bid(self.business_id)
        # validate_pid(self.oib)
        pass
