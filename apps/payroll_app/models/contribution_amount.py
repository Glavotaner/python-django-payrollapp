from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import Contribution


class ContributionAmount(models.Model):
    contribution_amount_id = models.AutoField(primary_key=True)

    contribution = models.ForeignKey(Contribution, on_delete=models.PROTECT, verbose_name=_('Contribution'))

    amount = models.FloatField(default=0, editable=False, verbose_name=_('Amount'))

    class Meta:
        verbose_name = _('Contribution amount')
        verbose_name_plural = _('Contribution amounts')

        db_table = 'contribution_amounts'

    def __str__(self):
        return f'{self.contribution.contribution_name} - {self.amount}'
