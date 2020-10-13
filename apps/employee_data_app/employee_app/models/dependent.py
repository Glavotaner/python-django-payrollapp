from django.db import models
from django.utils.translation import gettext_lazy as _
from .person import Person

class Dependent(Person):

    child = models.BooleanField(default=False, verbose_name = _('Child'))

    # FOREIGN KEYS
    dependent_of = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name = _('Dependent of'))

    class Meta:
        verbose_name = _('Dependent')
        verbose_name_plural = _('Dependents')


    def __str__(self):
        return f"{self.pid}"
