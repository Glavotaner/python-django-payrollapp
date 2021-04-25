from django.test import TestCase

from apps.employee_data_app.employee_app.models import Employee, Dependent
from . import load_fixtures
from .setUp import _set_up


class DeductiblesTests(TestCase):
    fixtures = load_fixtures.load_fixtures()

    def setUp(self):
        _set_up()

        self.employee = Employee.objects.get(oib="38263212114")

    def test_dependents(self):
        num_deps = self.employee.no_dependents

        self.assertEqual(num_deps, 4)

    def test_children(self):
        num_children = self.employee.no_children

        self.assertEqual(num_children, 4)

    def test_deps_disabled(self):
        num_disabled = self.employee.no_dependents_disabled

        self.assertEqual(num_disabled, 4)

    def test_deps_disabled_self(self):
        self.employee.disability = 'I'
        self.employee.save(update_fields=['disability'])

        num_disabled = self.employee.no_dependents_disabled

        self.assertEqual(num_disabled, 5)

    def test_deps_disabled_100(self):
        num_disabled_100 = self.employee.no_dependents_disabled_100

        self.assertEqual(num_disabled_100, 1)

    def test_delete(self):
        Dependent.objects.get(oib="38263212119").delete()

        self.employee = Employee.objects.get(oib="38263212114")

        self.assertEqual(self.employee.no_children, 3)
        self.assertEqual(
            self.employee.no_dependents, 4)
        self.assertEqual(
            self.employee.no_dependents_disabled, 3)
        self.assertEqual(
            self.employee.no_dependents_disabled_100, 1)
