from django.db import models
from django.utils.translation import gettext_lazy as _


from .person import Person
from apps.third_parties_app.models import Address
from apps.third_parties_app.models import Bank
from apps.employee_data_app.employment_app.models import Contract
from apps.calculation_data_app.models import ContributionsModality
from apps.general_services.validators.id_validators import validate_iban
from apps.general_services.validators.person_validation import validate_age
from apps.employee_data_app.employee_app.services.var_calculation import _employment_duration


class Employee(Person, Address):
    
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

        get_latest_by = 'employee_since'
        

    # DEPENDENTS
    no_children = models.IntegerField(
        verbose_name=_('Number of children'), default=0, editable=False)
    no_dependents = models.IntegerField(
        verbose_name=_('Number of dependents'), default=0, editable=False)
    no_dependents_disabled = models.IntegerField(
        verbose_name=_('Number of disabled dependents'), default=0, editable=False)
    no_dependents_disabled_100 = models.IntegerField(
        verbose_name=_('Number of 100% disabled dependents'), default=0, editable=False)
    

    iban = models.CharField(unique=True, verbose_name='IBAN', max_length=34)

    # FIRST EMPLOYMENT DATA
    first_employment = models.BooleanField(
        default=True, verbose_name=_('First employment'), db_index=True, blank=True, null=True)
    first_employment_with_company = models.BooleanField(
        default=True, verbose_name=_('First employment with company'), db_index=True, blank=True, null=True)

    employee_since = models.DateField(
        verbose_name=_('Employee since'), auto_now_add=True)
    employment_duration = models.CharField(verbose_name = _('Employment duration'), default="000000", editable = False, max_length = 8)


    # FOREIGN KEYS
    employee_bank = models.ForeignKey(to=Bank, verbose_name=_('Bank'), on_delete=models.DO_NOTHING)
    contributions_model = models.ForeignKey(ContributionsModality, on_delete=models.DO_NOTHING, verbose_name=_('Contributions model'))

    signed_contract = models.OneToOneField(
        to=Contract, verbose_name=_('Contract'), on_delete=models.CASCADE)
    

    def clean(self):
        validate_age(self.date_of_birth)
        # validate_iban(self.iban)
         

    def save(self, *args, **kwargs):       
        super(Employee, self).save(*args, **kwargs)
    


    def __str__(self):
        return f"{self.pid}"
