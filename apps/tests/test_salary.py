from typing import List

from django.test import TestCase
from django.db.models import ObjectDoesNotExist

from apps.employee_data_app.employee_app.models import Employee
from apps.payroll_app.models import Labour, Payroll
from apps.payroll_app.models import WageParameters
from .load_fixtures import load_fixtures
from .setUp import _set_up
from datetime import date


class TestSalary(TestCase):
    fixtures: List[str] = load_fixtures()

    def setUp(self) -> None:
        _set_up()

        Labour.set_labour(
            2021, 4, 168
        )

        self.labour_data = Labour.objects.get(pk=1)

        self.employee = Employee.objects.get(oib='38263212114')
        self.wage_params = WageParameters.objects.get(pk=1)
        Payroll.calculate_payrolls(date.today(), 2021, 4)
        self.payroll = Payroll.objects.get(pk=1)

    def test_payroll_exists(self):
        payroll = Payroll.objects.get(pk=1)
        self.assertIsNotNone(payroll)

    def test_reg_salary(self):
        salary: float = 5600
        self.assertEqual(salary, self.payroll.gross_salary)

    def test_min_salary(self):
        salary: float = 4250
        self.assertEqual(salary, 4250)

    def test_below_min(self):
        salary: float = 4000
        self.assertEqual(salary, 4250)

    def test_0(self):
        salary: float = 0
        self.assertEqual(salary, 4250)
