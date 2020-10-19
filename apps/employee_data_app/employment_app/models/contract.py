from django.db import models
from django.utils.translation import gettext_lazy as _
from . import ContractType, Position

class Contract(models.Model):


    contract_type = models.ForeignKey(
        ContractType, verbose_name = _('Contract type'), on_delete=models.DO_NOTHING)
    position = models.ForeignKey(
        Position, verbose_name = _('Position'), on_delete=models.DO_NOTHING)
    sign_date = models.DateField(verbose_name = _('Sign date'))
    expiration_date = models.DateField(
        verbose_name = _('Expiration date'))

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')
        get_latest_by = 'sign_date'

    def __str__(self):

        if self.expiration_date:
            return f"{self.contract_type.contract_type} contract | Signed: {self.sign_date} - Expires on: {self.expiration_date}"

        return f"{self.contract_type.contract_type} contract | Signed: {self.sign_date}"