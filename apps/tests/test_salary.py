from datetime import date

from django.test import TestCase
from .load_fixtures import load_fixtures
from .setUp import _set_up

from apps.payroll_app.models import Labour
from apps.payroll_app.services.calculations.salary_calculation import SalaryCalculated
from apps.calculation_data_app.models import WageParametersModel, HourFund
from apps.employee_data_app.employee_app.models import Employee


class TestSalary(TestCase):
    fixtures = load_fixtures()

    def setUp(self) -> None:
        _set_up()

        HourFund.objects.create(
            year=2021,
            month=3,
            total_hours=168
        ).save()

        Labour.set_labour(
            date(2021, 3, 22), date(2021, 3, 22), date(2021, 5, 1),
            overtime=16,
            night=0,
            sunday=6,
            special=0
        )

        self.labour_data = Labour.objects.get(id=1)
        self.employee = Employee.objects.get(pid='38263212114')
        self.wage_params = WageParametersModel.objects.get(id=1)
        #self.calculated_salary = SalaryCalculated()

    def test_reg_salary(self):
        salary: float = 5600

        self.assertEqual(salary, 5000)

    def test_min_salary(self):
        salary: float = 4250

        self.assertEqual(salary, 4250)

    def test_below_min(self):
        salary: float = 4000

        self.assertEqual(salary, 4250)

    def test_0(self):
        salary: float = 0

        self.assertEqual(salary, 4250)
