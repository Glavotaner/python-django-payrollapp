from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.employee_data_app.employee_app.models import Employee


class Labour(models.Model):

    

    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, db_index=True, verbose_name = _('Employee'))

    @property
    def labour_period(self):
        return f"{self.labour_start_date} to {self.labour_end_date}"

    labour_start_date = models.DateField(verbose_name = _('Labour start date'))
    labour_end_date = models.DateField(verbose_name = _('Labour end date'))
    regular_hours = models.PositiveIntegerField(verbose_name = _('Regular hours'))
    overtime_hours = models.PositiveIntegerField(verbose_name = _('Overtime hours'))
    special_hours = models.PositiveIntegerField(verbose_name = _('Holiday hours'))

    class Meta:
        verbose_name = _("Labour data")
        verbose_name_plural = _("Labour data")

    def __str__(self):
        return f"{_('Employee ID')}: {self.employee.pid} | {_('Labour period')}: {self.labour_period}"