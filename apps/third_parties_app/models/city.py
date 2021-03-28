from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.general_services.validators.general_validation import validate_gte


class City(models.Model):
    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    iban = models.CharField(
        max_length=34,
        verbose_name='IBAN',
        null=True
    )

    joppd = models.CharField(
        max_length=5,
        verbose_name='JOPPD',
        primary_key=True
    )

    city_name = models.CharField(
        max_length=80,
        verbose_name=_('City name')
    )

    postal_code = models.CharField(
        verbose_name=_('Postal code'),
        max_length=5
    )

    tax_rate = models.FloatField(
        verbose_name=_('Tax rate'),
        default=0.00,
        help_text=_('Input city tax rate as a decimal number')
    )

    def clean(self):
        # validate_city_id(self.joppd)
        # validate_iban(self.iban)
        # validate_gte(self.tax_rate, 'Tax rate')
        # validate_gte(self.tax_rate, 0, '0')
        pass

    def __str__(self):
        return f"""{self.city_name}"""
