from datetime import date
from typing import List

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class DeductiblesModel(models.Model):

    deductibles_model_id = models.AutoField(primary_key=True)

    base_deductible = models.FloatField(
        verbose_name=_('Base deductible'),
        help_text=_('Legal base deductible amount'),
        default=2500
    )

    personal_deductible_coef = models.FloatField(
        verbose_name=_('Personal deductible coef'),
        help_text=_('Legal personal deductible coefficient'),
        default=1.6
    )

    dependent = models.FloatField(
        verbose_name=_('Dependent deductible coef'),
        help_text=_('Dependent deductible coefficient'),
        default=0.7
    )

    first_child = models.FloatField(verbose_name=_('First child'), default=0.7)
    second_child = models.FloatField(
        verbose_name=_('Second child'), default=1.0)
    third_child = models.FloatField(verbose_name=_('Third child'), default=1.4)
    fourth_child = models.FloatField(
        verbose_name=_('Fourth child'), default=1.9)
    fifth_child = models.FloatField(verbose_name=_('Fifth child'), default=2.5)
    sixth_child = models.FloatField(verbose_name=_('Sixth child'), default=3.2)
    seventh_child = models.FloatField(
        verbose_name=_('Seventh child'), default=4.0
    )
    eighth_child = models.FloatField(
        verbose_name=_('Eighth child'), default=4.9
    )
    ninth_child = models.FloatField(verbose_name=_('Ninth child'), default=5.9)

    multiplication_coef = models.FloatField(
        verbose_name=_('Multiplication coef'), default=1.1
    )

    disabled_dependent_i = models.FloatField(
        verbose_name=_('Disabled dependent'), default=0.4
    )
    disabled_dependent_i100 = models.FloatField(
        verbose_name=_('100% disabled dependent'), default=1.5
    )

    valid_from = models.DateField(
        verbose_name=_('Valid from'), default=now
    )

    class Meta:
        verbose_name = _('Deductible')
        verbose_name_plural = _('Deductibles')
        get_latest_by = 'valid_from'

        db_table = 'deductibles_models'

    def __str__(self):
        return f"{self.base_deductible} | {self.personal_deductible_coef} || \
            {self.valid_from}"

    @staticmethod
    def get_valid_deductibles_model(target_date: date) -> List['DeductiblesModel']:
        return DeductiblesModel.objects.raw("""SELECT * FROM deductibles_models 
                                                WHERE valid_from = (SELECT MAX(valid_from) FROM deductibles_models
                                                WHERE valid_from <= %s)""", target_date)
