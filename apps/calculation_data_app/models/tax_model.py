from datetime import date
from typing import List

from django.db import models
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

    def __str__(self):
        return f'{self.valid_from}'

    @staticmethod
    def get_valid_tax_model(target_date: date) -> List['TaxModel']:
        return TaxModel.objects.raw("""SELECT * FROM tax_models 
                                                    WHERE valid_from = (SELECT MAX(valid_from) FROM tax_models
                                                    WHERE valid_from <= %s)""", target_date)
