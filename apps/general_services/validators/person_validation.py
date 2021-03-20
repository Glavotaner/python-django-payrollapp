from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_age(dob):
    today = date.today()
    try:
        birthday = dob.replace(year=today.year)

    except ValueError:
        birthday = dob.replace(year=today.year,
                               month=dob.month + 1, day=1)

    if birthday > today:
        _age = today.year - dob.year - 1
    else:
        _age = today.year - dob.year

    if 0 < _age < 18:
        raise ValidationError(_('Employee cannot be underage'))

    if _age < 0:
        raise ValidationError(_('Date of birth cannot be in the future'))
