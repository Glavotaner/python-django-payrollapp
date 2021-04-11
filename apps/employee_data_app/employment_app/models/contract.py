from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .contract_type import ContractType
from .position import Position


class Contract(models.Model):

    contract_id = models.AutoField(primary_key=True)

    contract_type = models.ForeignKey(
        ContractType,
        verbose_name=_('Contract type'),
        on_delete=models.DO_NOTHING
    )
    position = models.ForeignKey(
        Position,
        verbose_name=_('Position'),
        on_delete=models.DO_NOTHING
    )

    multiplier = models.FloatField(
        verbose_name=_('Multiplier'),
        default=1.00
    )

    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(
        verbose_name=_('Expiration date'),
        null=True, blank=True
    )

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

        get_latest_by = 'sign_date'

        db_table = 'contracts'

    def __str__(self):

        if self.end_date:
            return f"{self.contract_type.contract_type_name} contract | Signed: {self.start_date} \
            - Expires on: {self.end_date}"

        return f"{self.contract_type.contract_type_name} contract | Signed: {self.start_date}"

    def clean(self):
        if self.multiplier < 0:
            raise ValidationError(_('Multiplier cannot be less than 0'))

        if self.start_date and self.contract_type.contract_type_name == _('Indefinite'):
            raise ValidationError(_('An indefinite contract cannot have an expiration date'))

        if self.end_date and self.end_date < self.start_date:
            raise ValidationError(_('The contract cannot expire before it is signed'))
