from django.db import models

from apps.employee_data_app.employee_app.models import Employee


class Labour(models.Model):

    class Meta:
        verbose_name_plural = "Labour data"

    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)

    @property
    def labour_period(self):
        return f"{self.labour_start_date} to {self.labour_end_date}"

    labour_start_date = models.DateField(verbose_name='Labour start date')
    labour_end_date = models.DateField(verbose_name='Labour end date')
    regular_hours = models.PositiveIntegerField(verbose_name='Regular hours')
    overtime_hours = models.PositiveIntegerField(verbose_name='Overtime hours')
    special_hours = models.PositiveIntegerField(verbose_name='Holiday hours')

    def __str__(self):
        return f"Employee ID: {self.employee.pid} | Labour period: {self.labour_period}"