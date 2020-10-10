import re
from django.core.exceptions import ValidationError


def validate_phone_number(phone_number):
    if re.search('^\d{3}-\d{3}-\d{4}$', phone_number):
        raise ValidationError(
            'Phone number must only contain numbers and +, () or / characters')
        

def validate_gte(value, validator, value_name_1, value_name_2 = None):
    if value < validator:
        raise ValidationError(f'{value_name_1} has to be equal to or greater than {value_name_2}')
        