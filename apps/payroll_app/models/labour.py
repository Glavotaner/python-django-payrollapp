from typing import List

from django.db import models, connection
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import HourFund
from apps.employee_data_app.employee_app.models import Employee
from apps.general_services.data.data_service import get_period_id
from apps.payroll_app.models import HourTypeAmount


class Labour(models.Model):
    labour_id = models.AutoField(primary_key=True)

    year = models.IntegerField(default=2021, verbose_name=_('Year'))
    month = models.IntegerField(default=1, verbose_name=_('Month'))

    employee = models.ForeignKey(
        Employee,
        on_delete=models.DO_NOTHING,
        verbose_name=_('Employee'),
        db_index=True,
        null=True
    )

    regular_hours = models.PositiveIntegerField(
        verbose_name=_('Regular hours'), default=0
    )

    class Meta:
        verbose_name = _("Labour data")
        verbose_name_plural = _("Labour data")

        db_table = 'labours'

    # def __str__(self) -> str:
    #     return f"{_('Employee ID')}: {self.employee.oib} | {_('Period ')}: {self.period_id}"

    @staticmethod
    def set_labour(year: int, month: int, regular_hours: int, other_hours: List[dict] = None,
                   employees: List['Employee'] = None) -> None:

        if employees:
            eligible_employees = employees
        else:
            eligible_employees = Employee.get_eligible_employees(year, month)

        for emp in eligible_employees:
            labour: Labour = Labour.objects.create(
                employee=emp,

                year=year,
                month=month,

                regular_hours=regular_hours
            )

            labour.save()

            if other_hours:
                for hour_type in other_hours:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                    INSERT INTO hour_type_amounts (hour_type_id, labour_id, amount)
                    VALUES (%s, %s, %s)""",
                                       params=[hour_type['id'], labour.labour_id, hour_type['amount']])

    @property
    def get_hours_fund(self) -> int:
        return HourFund.objects.get(year=self.year, month=self.month).total_hours

    @property
    def hour_type_amounts(self) -> List[HourTypeAmount]:
        return HourTypeAmount.objects.filter(labour=self)

    @property
    def period_id(self) -> str:
        return get_period_id(self.year, self.month)

    @property
    def below_fund(self):
        return self.regular_hours < self.get_hours_fund
