from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from .person import Person
from .employee import Employee
from ..services.dependents_calculation import delete_from_employee, save_to_employee


class Dependent(Person):

    class Meta:
        verbose_name = _('Dependent')
        verbose_name_plural = _('Dependents')

    child = models.BooleanField(default=False, verbose_name=_('Child'))

    child_in_line = models.IntegerField(
        verbose_name=_('Child in line'),
        default=1,
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

    def clean(self):
        if not self.child and self.child_in_line:
            raise ValidationError(
                _('A dependent cannot have birth order data \
                    if they are not a child')
            )

    def save(self, *args, **kwargs):
        try:
            old_dep = Dependent.objects.get(pid=self.pid)

            delete_from_employee(old_dep)

            save_to_employee(self)

        except:
            save_to_employee(self)

        super(Dependent, self).save(*args, **kwargs)

    def delete(self):

        delete_from_employee(self)

        super(Dependent, self).delete()

    def __str__(self):
        return f"{self.pid}"
