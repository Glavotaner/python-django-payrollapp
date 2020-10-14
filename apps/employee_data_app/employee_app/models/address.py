from typing import Any
from django.db import models
from django.contrib import admin

import re
from datetime import timezone, date
from apps.third_parties_app.models import City
from django.core.exceptions import ValidationError
from apps.general_services.validators.general_validation import validate_phone_number
from django.utils.translation import gettext_lazy as _


class AbstractAddress(models.Model):

    class Meta:
        abstract = True

    street_name = models.CharField(max_length=20, verbose_name=_('Street name'))
    street_number = models.IntegerField(verbose_name=_('Street number'))
    city = models.ForeignKey(
        City, verbose_name=_('City name'), on_delete=models.DO_NOTHING)

    phone_number = models.CharField(max_length=15, verbose_name=_('Phone number'))

    def clean(self):

        validate_phone_number(self.phone_number)


class Address(AbstractAddress):

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


    def __str__(self):
        return f"""{self.street_name} {self.street_number}, {self.city.postal_code} {self.city}"""