from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import ContractType, Position

class Contract(models.Model):
    
    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')
        get_latest_by = 'sign_date'


    contract_type = models.ForeignKey(
        ContractType, 
        verbose_name = _('Contract type'), 
        on_delete=models.DO_NOTHING
        )
    position = models.ForeignKey(
        Position, 
        verbose_name = _('Position'), 
        on_delete=models.DO_NOTHING
        )
    
    multiplier = models.FloatField(
        verbose_name=_('Multiplier'), 
        default=1.00
        )
    
    sign_date = models.DateField(verbose_name = _('Sign date'))
    
    expiration_date = models.DateField(
        verbose_name = _('Expiration date'), 
        null=True, blank=True
        )
    
    def clean(self):
        if self.multiplier < 0:
            raise ValidationError(_('Multiplier cannot be less than 0'))
        
        if self.expiration_date and self.contract_type.contract_type == _('Indefinite'):
            raise ValidationError(_('An indefinite contract cannot have an expiration date'))
        
        if self.expiration_date < self.sign_date:
            raise ValidationError(_('The contract cannot expire before it is signed'))


    def __str__(self):

        if self.expiration_date:
            return f"{self.contract_type.contract_type} contract | Signed: {self.sign_date} - Expires on: {self.expiration_date}"

        return f"{self.contract_type.contract_type} contract | Signed: {self.sign_date}"