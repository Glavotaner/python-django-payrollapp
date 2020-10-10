from typing import Any
from django.db import models
from django.contrib import admin

import re
from datetime import timezone, date
from apps.third_party.city.models import City
from django.core.exceptions import ValidationError
from apps.general_services.validators.general_validation import validate_phone_number


class AbstractAddress(models.Model):

    class Meta:
        abstract = True

    street_name = models.CharField(max_length=20, verbose_name='Street name')
    street_number = models.IntegerField(verbose_name='Street number')
    city = models.ForeignKey(
        City, verbose_name='City name', on_delete=models.DO_NOTHING)

    phone_number = models.CharField(max_length=15, verbose_name='Phone number')

    def clean(self):

        validate_phone_number(self.phone_number)


class Address(AbstractAddress):

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"""{self.street_name} {self.street_number}, {self.postal_code} {self.city}"""