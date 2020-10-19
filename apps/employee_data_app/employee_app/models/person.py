from typing import Any
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

import re
from datetime import timezone, date
from apps.third_parties_app.models import City
from django.core.exceptions import ValidationError
from apps.general_services.validators.id_validators import validate_pid
from apps.general_services.validators.general_validation import validate_phone_number

class AbstractPerson(models.Model):

    class Meta:
        abstract = True

    # DISABILITY ENUM
    disability = [
        (_('D'), _('Disabled')),
        (_('D100'), _('100% disabled')),
        (_('N'), _('None'))
    ]

    pid = models.CharField(primary_key=True, max_length=11,
                           verbose_name=_('PID'))
    first_name = models.CharField(max_length=30, verbose_name = _('First name'))
    last_name = models.CharField(max_length=20, verbose_name = _('Last name'))
    date_of_birth = models.DateField(verbose_name = _('Date of birth'))
    age = models.IntegerField(verbose_name = _('Age'), editable = False)
    ageplus1 = models.IntegerField(editable = False)
    disability = models.CharField(
        choices=disability, max_length=4, verbose_name = _('Disability'), default='N')

    def clean(self):

        #validate_pid(self.pid)
        pass

    def save(self):
        self.age = 20
        self.ageplus1 = self.age + 1
        super(AbstractPerson, self).save()

class Person(AbstractPerson):

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}"""
