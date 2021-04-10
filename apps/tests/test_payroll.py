from datetime import date
from typing import List, TYPE_CHECKING

from django.test import TestCase

if TYPE_CHECKING:
    from ..employee_data_app.employee_app.models import Employee
    from ..payroll_app.models import Labour

from apps.tests import setUp, load_fixtures
from ..employee_data_app.employee_app.models import Employee
from ..payroll_app.models import Labour
from apps.calculation_data_app.models import HourFund


class TestPayroll(TestCase):
    fixtures = load_fixtures.load_fixtures()

    def setUp(self) -> None:
        setUp._set_up()

        HourFund.objects.create(
            year=2021,
            month=3,
            total_hours=168
        ).save()

    def test_eligible(self):
        eligible: List['Employee'] = Employee.get_eligible_employees(date(2021, 3, 22), date(2021, 5, 1))

        self.assertEqual(len(eligible), 1)

    def test_labour(self):
        Labour.set_labour(
            date(2021, 3, 22), date(2021, 3, 22), date(2021, 5, 1),
            overtime=16,
            sunday=6,
            night=0,
            special=0
        )

        self.assertEqual(len(Labour.objects.all()), 1)
        self.assertEqual(Labour.objects.get(labour_period='38263212114 - 2021-05-01').regular_hours, 168)
