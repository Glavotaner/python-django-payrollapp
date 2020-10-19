from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.employee_data_app.employee_app.models import Employee


class Labour(models.Model):


    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, db_index=True, verbose_name = _('Employee'))
    labour_period = models.CharField(verbose_name=_('Labour period ID'), editable = False, unique = True, max_length = 15)
    
    labour_start_date = models.DateField(verbose_name = _('Labour start date'))
    labour_end_date = models.DateField(verbose_name = _('Labour end date'))
    
    regular_hours = models.PositiveIntegerField(verbose_name = _('Regular hours'))
    overtime_hours = models.PositiveIntegerField(verbose_name = _('Overtime hours'), default = 0)
    special_hours = models.PositiveIntegerField(verbose_name = _('Holiday hours'), default = 0)

    class Meta:
        verbose_name = _("Labour data")
        verbose_name_plural = _("Labour data")

    def save(self):
        self.labour_period = str(self.employee.pid[:11]) + ' - ' + str(self.labour_end_date)

    def __str__(self):
        return f"{_('Employee ID')}: {self.employee.pid} | {_('Labour period')}: {self.labour_period}"
