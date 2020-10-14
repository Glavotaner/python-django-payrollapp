from os import truncate
from django.db import models
from .dependent import Dependent
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from datetime import date
import re

from .person import Person
from .address import Address
from apps.third_parties_app.models import Bank
from apps.employee_data_app.employment_app.models import Contract
from apps.calculation_data_app.models import ContributionsModality, TaxModel
from django.core.exceptions import ValidationError
from apps.general_services.validators.id_validators import validate_iban
from apps.general_services.validators.person_validation import validate_age
from apps.employee_data_app.employee_app.services.dependents_calculator import *


class Employee(Person, Address):

    # PROPERTIES
    # DEPENDENTS
    @property
    def no_children(self):
        return calculate_no_children(self.pid)

    @property
    def no_dependents(self):
        return calculate_no_dependents(self.pid)

    @property
    def no_dependents_disabled(self):
        return caluclate_no_dependents_disabled(self.pid)

    @property
    def no_dependents_disabled_100(self):
        return calculate_no_dependents_disabled_100(self.pid)

    iban = models.CharField(unique=True, verbose_name='IBAN', max_length=34)

    # FIRST EMPLOYMENT DATA
    first_employment = models.BooleanField(
        default=True, verbose_name=_('First employment'), db_index=True)
    first_employment_with_company = models.BooleanField(
        default=True, verbose_name=_('First employment with company'), db_index=True)

    employee_since = models.DateField(
        verbose_name=_('Employee since'), auto_now_add=True)

    # FOREIGN KEYS
    employee_bank = models.ForeignKey(
        to=Bank, verbose_name=_('Bank'), on_delete=models.SET_NULL, null = True)

    contributions_model = models.ForeignKey(
        ContributionsModality, on_delete=models.SET_NULL, verbose_name=_('Contributions model'), null = True)

    signed_contract = models.OneToOneField(
        to=Contract, verbose_name=_('Contract'), on_delete=models.CASCADE)

    def clean(self):
        validate_age(self.date_of_birth)
        # validate_iban(self.iban)

    def delete(self):
        keep_parents = True

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

        get_latest_by = 'employee_since'

    def __str__(self):
        return f"{self.pid}"
