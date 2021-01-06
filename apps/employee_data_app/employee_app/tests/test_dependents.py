from datetime import date
from django.test import TestCase
from apps.employee_data_app.employee_app.models import Employee, Dependent

from .setUp import dependentsSetUp


class DeductiblesTests(TestCase):

    def setUp(self):

        dependentsSetUp(self)
        

    def test_dependents(self):
        num_deps = Employee.objects.get(pid="38263212113").no_dependents

        self.assertEqual(num_deps, 4)

    def test_children(self):
        num_children = Employee.objects.get(pid="38263212113").no_children
        
        self.assertEqual(num_children, 4)

    def test_deps_disabled(self):
        num_disabled = Employee.objects.get(
            pid="38263212113").no_dependents_disabled
        
        self.assertEqual(num_disabled, 3)

    def test_deps_disabled_100(self):
        num_disabled_100 = Employee.objects.get(
            pid="38263212113").no_dependents_disabled_100
        
        self.assertEqual(num_disabled_100, 1)
        
    def test_delete(self):
        Dependent.objects.get(pid="38263212119").delete()
        
        self.assertEqual(Employee.objects.get(pid="38263212113").no_children, 3)
        self.assertEqual(
            Employee.objects.get(pid="38263212113").no_dependents, 4)
        self.assertEqual(
            Employee.objects.get(pid="38263212113").no_dependents_disabled, 3)
        self.assertEqual(
            Employee.objects.get(pid="38263212113").no_dependents_disabled_100,\
                1)
