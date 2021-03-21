import django.utils.timezone
from django.test import TestCase

from apps.calculation_data_app.services.deductibles_calculation import DeductibleCalculated, get_deductibles_model
from apps.employee_data_app.employee_app.models import Employee
from . import setUp, load_fixtures


class TestDeductibles(TestCase):
    fixtures = load_fixtures.load_fixtures()

    def setUp(self) -> None:
        setUp._set_up()

        self.employee: Employee = Employee.objects.get(pid='38263212114')

        self.deductible_calculated: DeductibleCalculated = DeductibleCalculated(
            get_deductibles_model(django.utils.timezone.datetime.today()),
            employee=self.employee
        )

    def test_personal_deductible(self):
        self.assertEqual(self.deductible_calculated.personal_deductible, 4000)

    def test_dependents_deductible(self):
        self.assertEqual(self.deductible_calculated.adults_deductible, 3500)

    def test_children_deductible(self):
        self.assertEqual(self.deductible_calculated.children_deductible, (1750 + 2500 + 3500 + 6250))

    def test_dependents_deductible_disabled(self):
        self.assertEqual(self.deductible_calculated.disabled_deductible, 3000)

    def test_dependents_deductible_disabled_100(self):
        self.assertEqual(self.deductible_calculated.disabled_100_deductible, 3750)

    def test_total_deductible(self):
        self.assertEqual(self.deductible_calculated.total_deductible, 31750 - 3500)
