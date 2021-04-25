from django.db import models
from django.utils.translation import gettext_lazy as _

from . import City


class Address(models.Model):
    street_name = models.CharField(
        verbose_name=_('Street name'), max_length=200
    )

    street_number = models.CharField(
        verbose_name=_('Street number'), max_length=10
    )

    city = models.ForeignKey(
        City, verbose_name=_('City name'),
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

        db_table = 'addresses'
