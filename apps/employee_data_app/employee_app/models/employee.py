from datetime import datetime, date

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from . import Employee

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import ContributionsModel, TaxBreakModel
from apps.employee_data_app.employment_app.models import Contract
# from apps.general_services.validators.id_validators import validate_iban, validate_bid
from apps.general_services.validators.person_validation import validate_age
from apps.third_parties_app.models import Address
from apps.third_parties_app.models import Bank
from .person import Person


class Employee(Person, Address):
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

        get_latest_by = 'employee_since'

    HRVI = models.FloatField(default=0)

    iban = models.CharField(unique=True, verbose_name='IBAN', max_length=34)

    protected_iban = models.CharField(unique=True, verbose_name='Protected IBAN', max_length=34)

    # EmployeeS
    no_children = models.IntegerField(
        verbose_name=_('Number of children'),
        default=0,
        editable=False
    )

    no_dependents = models.IntegerField(
        verbose_name=_('Number of Employees'),
        default=0, editable=False
    )

    no_dependents_disabled = models.IntegerField(
        verbose_name=_('Number of disabled Employees'),
        default=0,
        editable=False
    )

    no_dependents_disabled_100 = models.IntegerField(
        verbose_name=_('Number of 100% disabled Employees'),
        default=0,
        editable=False
    )

    # FIRST EMPLOYMENT DATA
    first_employment = models.BooleanField(
        default=True,
        verbose_name=_('First employment'),
        db_index=True,
        blank=True, null=True
    )

    first_employment_with_company = models.BooleanField(
        default=True,
        verbose_name=_('First employment with company'),
        db_index=True,
        blank=True, null=True
    )

    employee_since = models.DateTimeField(
        verbose_name=_('Employee since'), auto_now_add=True
    )

    # FOREIGN KEYS
    employee_bank = models.ForeignKey(
        related_name='bank',
        to=Bank, verbose_name=_('Bank'),
        on_delete=models.DO_NOTHING
    )

    employee_protected_bank = models.ForeignKey(
        related_name='protected_bank',
        to=Bank, verbose_name=_('Protected account bank'),
        on_delete=models.DO_NOTHING
    )

    contributions_model = models.ForeignKey(
        ContributionsModel,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Contributions model')
    )

    signed_contract = models.OneToOneField(
        to=Contract,
        verbose_name=_('Contract'),
        on_delete=models.CASCADE
    )

    tax_breaks = models.ManyToManyField(TaxBreakModel)

    @staticmethod
    def get_eligible_employees(start_date: date, end_date: date) -> List['Employee']:
        sql: str = """SELECT e.* FROM employee_app_employee AS e
        INNER JOIN employment_app_contract AS c
            ON c.id = e.signed_contract_id
        WHERE c.sign_date <= %s AND (c.expiration_date >= %s OR c.expiration_date IS NULL)"""

        return Employee.objects.raw(sql, [start_date, end_date])

    @property
    def employment_duration(self):
        return datetime.now() - self.employee_since

    @property
    def employee_bank_name(self):
        return self.employee_bank.bank_name

    def clean(self):
        validate_age(self.date_of_birth)
        # validate_iban(self.iban)

    def __str__(self):
        return f"{self.pid}"
