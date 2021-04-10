from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

        db_table = 'cities'

    city_id = models.AutoField(primary_key=True)

    iban = models.CharField(
        max_length=22,
        verbose_name='IBAN'
    )

    joppd = models.CharField(
        max_length=5,
        verbose_name='JOPPD'
    )

    city_name = models.CharField(
        max_length=200,
        verbose_name=_('City name')
    )

    postal_code = models.CharField(
        verbose_name=_('Postal code'),
        max_length=5
    )

    tax_rate = models.FloatField(
        verbose_name=_('Tax rate'),
        default=0.00,
        help_text=_('City tax rate')
    )

    def clean(self):
        # validate_city_id(self.joppd)
        # validate_iban(self.iban)
        # validate_gte(self.tax_rate, 'Tax rate')
        # validate_gte(self.tax_rate, 0, '0')
        pass

    def __str__(self):
        return f"""{self.city_name}"""
