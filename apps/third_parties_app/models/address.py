from django.db import models

from . import City
from apps.general_services.validators.general_validation import validate_phone_number
from django.utils.translation import gettext_lazy as _
from apps.general_services.validators.general_validation import validate_phone_number


class Address(models.Model):

    class Meta:
        abstract = True

        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    street_address = models.CharField(
        verbose_name=_('Street address'), max_length=300
    )

    city = models.ForeignKey(
        City, verbose_name=_('City name'),
        on_delete=models.DO_NOTHING
    )

    phone_number = models.CharField(
        max_length=15,
        verbose_name=_('Phone number'),
        null=True
    )

    def clean(self):
        validate_phone_number(self.phone_number)
