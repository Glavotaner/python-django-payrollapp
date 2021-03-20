from django.test import TestCase

from apps.employee_data_app.employee_app.models import Employee, Dependent
from .setUp import _set_up


class DeductiblesTests(TestCase):
    fixtures = [
        'apps/calculation_data_app/fixtures/deductibles_model_fixtures.json',
        'apps/calculation_data_app/fixtures/contributions_model_fixtures.json',
        'apps/third_parties_app/fixtures/bank_fixtures.json',
        'apps/third_parties_app/fixtures/city_fixtures.json',
        'apps/employee_data_app/employment_app/fixtures/position_fixtures.json',
        'apps/employee_data_app/employment_app/fixtures/contract_type_fixtures.json',
    ]

    def setUp(self):
        _set_up()

        self.employee = Employee.objects.get(pid="38263212114")

    def test_dependents(self):
        num_deps = self.employee.no_dependents

        self.assertEqual(num_deps, 2)

    def test_children(self):
        num_children = self.employee.no_children

        self.assertEqual(num_children, 4)

    def test_deps_disabled(self):
        num_disabled = self.employee.no_dependents_disabled

        self.assertEqual(num_disabled, 3)

    def test_deps_disabled_self(self):
        self.employee.disability = 'D'
        self.employee.save(update_fields=['disability'])

        num_disabled = self.employee.no_dependents_disabled

        self.assertEqual(num_disabled, 3)

    def test_deps_disabled_100(self):
        num_disabled_100 = self.employee.no_dependents_disabled_100

        self.assertEqual(num_disabled_100, 1)

    def test_delete(self):
        Dependent.objects.get(pid="38263212119").delete()

        self.employee = Employee.objects.get(pid="38263212114")

        self.assertEqual(self.employee.no_children, 3)
        self.assertEqual(
            self.employee.no_dependents, 2)
        self.assertEqual(
            self.employee.no_dependents_disabled, 3)
        self.assertEqual(
            self.employee.no_dependents_disabled_100, 1)