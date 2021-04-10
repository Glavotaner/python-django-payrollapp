from django.db import models
from django.utils.translation import gettext_lazy as _

from ..services.calculations.var_calculation import get_age


class Person(models.Model):
    class Meta:
        abstract = True

        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    # DISABILITY ENUM
    disability = (
        (_('I'), _('I')),
        (_('I*'), _('I*')),
        (_('N'), _('None'))
    )

    oib = models.CharField(
        max_length=11,
        verbose_name=_('OIB'),
        help_text=_('Input valid PID'),
        unique=True
    )

    first_name = models.CharField(
        max_length=120,
        verbose_name=_('First name')
    )

    last_name = models.CharField(
        max_length=120,
        verbose_name=_('Last name')
    )

    date_of_birth = models.DateField(verbose_name=_('Date of birth'))

    disability = models.CharField(
        choices=disability,
        max_length=2,
        verbose_name=_('Disability'),
        default='N'
    )

    @property
    def age(self):
        return get_age(self)

    def clean(self):
        # validate_pid(self.pid)
        # validate_phone_number(self.phone_number)

        pass
