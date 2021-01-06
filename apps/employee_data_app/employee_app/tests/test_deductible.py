from django.test import TestCase

from datetime import date

from apps.third_parties_app.models import City, Bank
from apps.calculation_data_app.models import ContributionsModel
from ...employment_app.models import Position, Contract, ContractType, contract_type
from ..models import Employee, Dependent
from apps.calculation_data_app.models import DeductiblesModel

from apps.payroll_app.services.calculations import deductibles_calculation
from ..tests.setUp import _setUp

class DeductibleTest(TestCase):
    
    
    def setUp(self):
        
        _setUp(self)
   
    
    def test_personal_deductible(self):       
        
        self.assertEqual(\
            self.personal_deductible_amount, 4000, \
                msg=f"Personal deductible is {self.personal_deductible_amount}, not 4000")   
    
    def test_dependents_deductible(self):        
        self.assertEqual(self.deductible_dependents, 4*1750)
        
    def test_children_deductible(self):
        self.assertEqual(self.deductible_children, 1750 + 2500 + 3500 + 4750)
        
    def test_deductible_dependents_disabled(self):
        self.assertEqual(self.deductible_dependents_disabled, 3*1000)
        
    def test_deductible_dependents_disabled_100(self):
        self.assertEqual(self.deductible_dependents_disabled_100, 3750) 
        
    def test_deductible_total(self):
        self.assertEqual(self.total_deductibles, 4000 + (4*1750) + (1750 + 2500 + 3500 + 4750) + (3*1000), 3750)
        
    def test_decrease_deductible(self):
        Dependent.objects.get(pid="38263212111").delete()
        
        self.assertEqual(self.deductible_children, 1750 + 2500 + 3500)
        self.assertEqual(self.total_deductibles, 4000 + (4*1750) + (1750 + 2500 + 3500) + (3*1000), 3750)