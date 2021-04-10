import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(phone_number):
    phone_number = phone_number.strip()

    if re.search('^[^0-9+-/]{17}$', phone_number):
        raise ValidationError(
            _('Phone number must not contain letters!'))


def validate_gte(value, validator, value_name_1, value_name_2=None):
    if value < validator:
        raise ValidationError(
            _(f'{value_name_1} has to be equal to or greater \
                than {value_name_2}')
        )
