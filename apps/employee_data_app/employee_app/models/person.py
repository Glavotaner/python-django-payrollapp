from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.general_services.validators.id_validators import validate_pid
from apps.employee_data_app.employee_app.services.var_calculation import _age


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

    pid = models.CharField(primary_key=True, max_length=11,
                           verbose_name=_('PID'))
    first_name = models.CharField(max_length=30, verbose_name=_('First name'), blank=True, null=True)
    last_name = models.CharField(max_length=20, verbose_name=_('Last name'), blank=True, null=True)
    date_of_birth = models.DateField(verbose_name=_('Date of birth'))
    age = models.IntegerField(verbose_name=_('Age'), editable=False)
    disability = models.CharField(
        choices=disability, max_length=4, verbose_name=_('Disability'), default='N')

    def clean(self):
        # validate_pid(self.pid)
        pass

    def save(self, *args, **kwargs):
        self.age = _age(self)
        super(Person, self).save(*args, **kwargs)
