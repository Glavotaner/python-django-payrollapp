from calendar import monthrange
from datetime import date, timedelta
from typing import List

from django.db import models
from django.db.models import Q, QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import ContributionsModel, TaxBreak
from apps.employee_data_app.employee_app.models import Dependent
from apps.employee_data_app.employee_app.services.calculations.dependents_calculation import update_employee
from apps.employee_data_app.employment_app.models import Contract
# from apps.general_services.validators.id_validators import validate_iban, validate_bid
from apps.general_services.validators.person_validation import validate_age
from apps.third_parties_app.models import Address, Bank
from .person import Person


class Employee(Person, Address):
    employee_id = models.AutoField(primary_key=True)

    hrvi = models.FloatField(default=0)

    iban = models.CharField(unique=True, verbose_name='IBAN', max_length=22)

    protected_iban = models.CharField(unique=True, verbose_name='Protected IBAN', max_length=22, null=True, blank=True)

    # Dependents
    no_children = models.IntegerField(
        verbose_name=_('Number of children'),
        default=0,
        editable=False
    )
    no_dependents = models.IntegerField(
        verbose_name=_('Number of dependents'),
        default=0, editable=False
    )
    no_dependents_disabled = models.IntegerField(
        verbose_name=_('Number of disabled dependents'),
        default=0,
        editable=False
    )
    no_dependents_disabled_100 = models.IntegerField(
        verbose_name=_('Number of 100% disabled dependents'),
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
        on_delete=models.DO_NOTHING,
        null=True, blank=True
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

    tax_breaks = models.ManyToManyField(TaxBreak)

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

        get_latest_by = 'employee_since'

        db_table = 'employees'

    def __str__(self):
        return f"{self.oib}"

    def clean(self):
        validate_age(self.date_of_birth)
        # validate_iban(self.iban)

    @staticmethod
    def get_eligible_employees(year: int, month: int) -> QuerySet['Employee']:
        start_date: date = date(year, month, 1)
        end_date: date = date(year, month, monthrange(year, month)[1])

        return Employee.objects.filter(
            (Q(signed_contract__start_date__lte=start_date) & (
                    Q(signed_contract__end_date__gte=start_date) | Q(signed_contract__end_date__isnull=True))
             ) |
            (Q(signed_contract__start_date__lte=end_date) & (
                    Q(signed_contract__end_date__gte=start_date) | Q(signed_contract__end_date__isnull=True))
             )
        )

    @property
    def employee_bank_name(self) -> str:
        return self.employee_bank.bank_name

    @property
    def employment_duration(self) -> timedelta:
        return date.today() - self.employee_since

    # CONTRACT DATA
    @property
    def contract_expired(self, target_date: date = None) -> bool:
        if not self.signed_contract.end_date:
            return False

        if target_date:
            return self.signed_contract.end_date > target_date

        return self.signed_contract.end_date > date.today()

    @property
    def employee_position(self) -> str:
        return self.signed_contract.position.position_name

    @property
    def employee_salary(self) -> float:
        return self.signed_contract.total_salary

    # DEPENDENTS
    @property
    def get_dependents(self) -> List['Dependent']:
        return Dependent.objects.filter(dependent_of=self)

    @property
    def get_children_list(self) -> QuerySet['Dependent']:
        return Dependent.objects.filter(dependent_of=self, child_in_line__isnull=False)

    @property
    def get_adult_dependents_count(self) -> int:
        return Dependent.objects.filter(dependent_of=self, child_in_line__isnull=True).count()

    @property
    def get_disabled_dependents_count(self) -> int:
        deps_count: int = Dependent.objects.filter(dependent_of=self, disability='I').count()

        return deps_count + 1 if self.disability == 'I' else deps_count

    @property
    def get_disabled_dependents_100_count(self) -> int:
        deps_count: int = Dependent.objects.filter(dependent_of=self, disability='I*').count()

        return deps_count + 1 if self.disability == 'I*' else deps_count


@receiver(post_save, sender=Employee)
def signal_update_employee(sender, instance: 'Employee', **kwargs):
    post_save.disconnect(signal_update_employee, sender=sender)
    update_employee(instance)
    post_save.connect(signal_update_employee, sender=sender)


post_save.connect(signal_update_employee, sender=Employee)
