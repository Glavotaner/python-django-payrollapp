# from apps.employee_data_app.employee_app.services.validation.validate_dependent import validate_child_no_order, \
# validate_child_order

from django.db import models
from django.utils.translation import gettext_lazy as _

from .employee import Employee
from .person import Person
from ..services.calculations.dependents_calculation import update_employee


class Dependent(Person):
    class Meta:
        verbose_name = _('Dependent')
        verbose_name_plural = _('Dependents')

        db_table = 'dependents'

    dependent_id = models.AutoField(primary_key=True)

    child_in_line = models.IntegerField(
        verbose_name=_('Child in line'),
        help_text=_('Number of child in order of birth, eg. 1st child = 1'),
        null=True,
        blank=True
    )

    # FOREIGN KEYS
    dependent_of = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_('Dependent of')
    )

    @property
    def parent_employee(self) -> Employee:
        return self.dependent_of

    def clean(self):
        # validate_child_no_order(self)
        # validate_child_order(self)
        pass

    def save(self, *args, **kwargs):
        super(Dependent, self).save()
        update_employee(self.parent_employee)

    def delete(self, *args, **kwargs):
        super(Dependent, self).delete()
        update_employee(self.parent_employee)

    def __str__(self):
        return f"{self.disability} || {self.child_in_line}"
