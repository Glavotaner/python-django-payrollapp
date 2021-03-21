from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.employee_data_app.employee_app.models import Employee
from apps.payroll_app.services.calculations.var_calculation import get_months_hours_fund


class Labour(models.Model):
    class Meta:
        verbose_name = _("Labour data")
        verbose_name_plural = _("Labour data")

    employee = models.ForeignKey(
        Employee,
        on_delete=models.DO_NOTHING,
        db_index=True,
        verbose_name=_('Employee')
    )

    labour_period = models.CharField(
        verbose_name=_('Labour period ID'),
        editable=False,
        unique=True,
        max_length=15
    )

    labour_start_date = models.DateField(verbose_name=_('Labour start date'))
    labour_end_date = models.DateField(verbose_name=_('Labour end date'))

    regular_hours = models.PositiveIntegerField(
        verbose_name=_('Regular hours'), default=0
    )
    overtime_hours = models.PositiveIntegerField(
        verbose_name=_('Overtime hours'), default=0
    )
    special_hours = models.PositiveIntegerField(
        verbose_name=_('Holiday hours'), default=0
    )

    @staticmethod
    def set_labour(_date: date, start_date: date, end_date: date, overtime: float, special: float):
        eligible_employees = Employee.get_eligible_employees(start_date, end_date)

        period_id = str(_date.year) + str(_date.month)

        hours_fund = get_months_hours_fund(start_date)

        # print(period_id)

        for emp in eligible_employees:
            Labour.objects.create(
                employee=emp,

                labour_start_date=start_date,
                labour_end_date=end_date,

                regular_hours=hours_fund,
                overtime_hours=overtime,
                special_hours=special,
            ).save()

    def save(self, *args, **kwargs):
        self.labour_period = str(self.employee.pid[:11]) + ' - ' + str(self.labour_end_date)
        super(Labour, self).save()

    def __str__(self):
        return f"{_('Employee ID')}: {self.employee.pid} | {_('Labour period')}: {self.labour_period}"
