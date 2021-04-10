import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_pid(pid: str):
    pid = pid.strip()

    if len(pid) != 11:
        raise ValidationError(_('PID is of an invalid length'))

    if re.search('[^0-9]', pid):
        raise ValidationError(_('PID is not entirely numeric'))

    control = int(pid[-1])
    previous_remainder = 0

    for i, num in enumerate(str(pid)):
        num = int(num)

        if i == 10:
            break

        if i == 0:
            num += 10
        else:
            num += previous_remainder

        if num % 10 == 0:
            num = 10
        else:
            num %= 10

        num *= 2

        num %= 11

        previous_remainder = num

    if not (11 - previous_remainder) % 10 == control:
        raise ValidationError(_('PID is invalid, please check your input'))


def validate_bid(bid):
    bid = bid.strip()

    if len(bid) != 8:
        raise ValidationError(_('Business ID number is of an invalid length'))
    if re.search('[^0-9]', bid):
        raise ValidationError(_('Businnes ID number is not entirely numeric'))

    control = int(bid[-1])

    _bid = bid[:-1]

    res = 0
    i = 8
    while i >= 2:
        res += (int(_bid[8 - i]) * i)

        i -= 1

    res %= 11

    if not (11 - res) % 10 == control:
        raise ValidationError(_('Business ID number is invalid'))


def validate_iban(iban):
    _country2length = dict(
        AL=28, AD=24, AT=20, AZ=28, BE=16, BH=22, BA=20, BR=29,
        BG=22, CR=21, HR=21, CY=28, CZ=24, DK=18, DO=28, EE=20,
        FO=18, FI=18, FR=27, GE=22, DE=22, GI=23, GR=27, GL=18,
        GT=28, HU=28, IS=26, IE=22, IL=23, IT=27, KZ=20, KW=30,
        LV=21, LB=28, LI=21, LT=20, LU=20, MK=19, MT=31, MR=27,
        MU=30, MC=27, MD=24, ME=22, NL=18, NO=15, PK=24, PS=29,
        PL=28, PT=25, RO=24, SM=27, SA=24, RS=22, SK=24, SI=19,
        ES=24, SE=24, CH=21, TN=24, TR=26, AE=23, GB=22, VG=24)

    _iban = iban.replace(' ', '').replace('\t', '')

    _iban = _iban.strip()

    if _iban[:2] not in _country2length.keys():
        raise ValidationError(_('IBAN country code invalid'))

    if not re.match(r'^[\dA-Z]+$', _iban):
        raise ValidationError(_('IBAN is not properly formatted'))

    if len(_iban) != _country2length[_iban[:2]]:
        raise ValidationError(_('IBAN country code is not the correct length'))

    _iban = _iban[4:] + _iban[:4]

    digits = int(''.join(str(int(ch, 36)) for ch in _iban))

    if not digits % 97 == 1:
        raise ValidationError(_('IBAN is invalid'))


def validate_city_id(city_id):
    # City ID VALIDATION

    city_id = city_id.strip()

    if len(city_id) != 5:
        raise ValidationError(_('City ID number is of an invalid length'))
    if re.search('[^0-9]', city_id):
        raise ValidationError(_('City ID number is not entirely numeric'))

    control = int(city_id[-1])

    _city_id = city_id[1:-1]

    res = 0
    i = 4
    while i >= 2:
        res += (int(_city_id[4 - i]) * i)

        i -= 1

    res %= 11

    if not (11 - res) % 10 == control:
        raise ValidationError(_('City ID number is invalid'))
