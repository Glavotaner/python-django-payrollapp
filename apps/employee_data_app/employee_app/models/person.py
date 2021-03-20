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
        (_('D'), _('Disabled')),
        (_('D100'), _('100% disabled')),
        (_('N'), _('None'))
    )

    pid = models.CharField(
        primary_key=True,
        max_length=11,
        verbose_name=_('PID')
    )

    first_name = models.CharField(
        max_length=30,
        verbose_name=_('First name'),
        blank=True, null=True
    )

    last_name = models.CharField(
        max_length=20,
        verbose_name=_('Last name'),
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(verbose_name=_('Date of birth'))

    disability = models.CharField(
        choices=disability,
        max_length=4,
        verbose_name=_('Disability'),
        default='N'
    )

    @property
    def age(self):
        return get_age(self)

    def clean(self):
        # validate_pid(self.pid)
        pass

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
