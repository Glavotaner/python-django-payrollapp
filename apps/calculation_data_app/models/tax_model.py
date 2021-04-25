from datetime import date

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import TaxBracket


class TaxModel(models.Model):
    tax_model_id = models.AutoField(primary_key=True)
    tax_brackets = models.ManyToManyField(TaxBracket, verbose_name=_('Tax brackets'))
    valid_from = models.DateField(verbose_name='Valid from')

    class Meta:
        verbose_name = 'Tax model'
        verbose_name_plural = 'Tax models'

        db_table = 'tax_models'

        get_latest_by = 'valid_from'

    def __str__(self):
        return f'{self.valid_from}'

    @staticmethod
    def get_valid_tax_model(target_date: date) -> 'TaxModel':
        return TaxModel.objects.filter(
            valid_from__lte=target_date
        ).latest()

    def get_tax_bracket(self, income: float) -> 'TaxBracket':
        return self.tax_brackets.filter(
            Q(amount_from__lte=income) &
            (Q(amount_to__gte=income) | Q(amount_to__isnull=True))
        ).get()
