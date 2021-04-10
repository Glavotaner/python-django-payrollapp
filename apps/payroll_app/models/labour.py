from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.general_services.data.data_service import get_period_id

from apps.calculation_data_app.models import HourFund
from apps.employee_data_app.employee_app.models import Employee
from apps.payroll_app.models import HourTypeAmount


class Labour(models.Model):
    class Meta:
        verbose_name = _("Labour data")
        verbose_name_plural = _("Labour data")

        db_table = 'labours'

    labour_id = models.AutoField(primary_key=True)

    year = models.IntegerField(default=2021, verbose_name=_('Year'))
    month = models.IntegerField(default=1, verbose_name=_('Month'))

    employee = models.ForeignKey(
        Employee,
        on_delete=models.DO_NOTHING,
        db_index=True,
        verbose_name=_('Employee')
    )

    regular_hours = models.PositiveIntegerField(
        verbose_name=_('Regular hours'), default=0
    )

    hour_type_amounts = models.ManyToManyField(HourTypeAmount, verbose_name=_('Other hours'))

    @property
    def get_hours_fund(self) -> int:
        return HourFund.objects.get(year=self.year, month=self.month)

    @property
    def period_id(self):
        return get_period_id(self.year, self.month)

    @staticmethod
    def set_labour(_date: date, year: int, month: int):
        eligible_employees = Employee.get_eligible_employees(year, month)

        hours_fund = HourFund.get_hour_fund_for_period(year, month)

        for emp in eligible_employees:
            Labour.objects.create(
                employee=emp,

                year=year,
                month=month,

                regular_hours=hours_fund
            ).save()

    def __str__(self):
        return f"{_('Employee ID')}: {self.employee.oib} | {_('Period ')}: {self.period_id}"
