from django.db import models
from django.utils.translation import gettext_lazy as _


class HourTypeAmount(models.Model):
    hour_type_amount_id = models.AutoField(primary_key=True)

    hour_type = models.ForeignKey('calculation_data_app.HourType', on_delete=models.PROTECT, verbose_name=_('Hour type'))
    labour = models.ForeignKey('Labour', on_delete=models.CASCADE, verbose_name=_('Labour'))

    amount = models.IntegerField(verbose_name=_('Amount'))

    class Meta:
        verbose_name = _('Hour type amount')
        verbose_name_plural = _('Hour type amounts')

        db_table = 'hour_type_amounts'

    def __str__(self):
        return f'{self.hour_type.hour_type_name} - {self.amount}'

    @staticmethod
    def get_payroll_hour_amounts(target_labour):
        return HourTypeAmount.objects.filter(labour=target_labour)

    @property
    def hour_type_name(self):
        return self.hour_type.hour_type_name
