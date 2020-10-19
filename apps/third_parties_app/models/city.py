from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.general_services.validators.general_validation import validate_gte
from apps.general_services.validators.id_validators import validate_iban, validate_city_id


class City(models.Model):

    iban = models.CharField(max_length=34, verbose_name='IBAN')
    joppd = models.CharField(
        max_length=5, verbose_name='JOPPD', primary_key=True)
    city_name = models.CharField(max_length=50, verbose_name = _('City name'))
    postal_code = models.PositiveIntegerField(verbose_name = _('Postal code'))
    tax_rate = models.FloatField(verbose_name = _('Tax rate'), default=0.00, help_text = _('Input city tax rate as a decimal number'))
    tax_break = models.FloatField(verbose_name = _('Tax break'), default=0.00, help_text = _('Input city tax break as a decimal number eg. tax_rate = 0.13, tax_break = 0.06: tax_rate = 0.07'))

    def clean(self):

        #validate_city_id(self.joppd)
        # validate_iban(self.iban)
        validate_gte(self.tax_rate, self.tax_break, 'Tax rate', 'Tax break')
        validate_gte(self.tax_rate, 0, '0')
        validate_gte(self.tax_break, 0, '0')

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return f"""{self.city_name}"""
