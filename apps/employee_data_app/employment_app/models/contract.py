from django.db import models
from . import ContractType, Position

class Contract(models.Model):

    class Meta:
        get_latest_by = 'sign_date'

    contract_type = models.ForeignKey(
        ContractType, verbose_name='Contract type', on_delete=models.DO_NOTHING)
    position = models.ForeignKey(
        Position, verbose_name='Position', on_delete=models.DO_NOTHING)
    sign_date = models.DateField(verbose_name='Sign date')
    expiration_date = models.DateField(
        verbose_name='Expiration date', blank=True, null=True)

    def __str__(self):

        if self.expiration_date:
            return f"{self.contract_type.contract_type} contract | Signed: {self.sign_date} - Expires on: {self.expiration_date}"

        return f"{self.contract_type.contract_type} contract | Signed: {self.sign_date}"