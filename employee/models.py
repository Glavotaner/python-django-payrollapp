from django.db import models

from common.models import Person, PersonalAddress
from bank.models import Bank


class PaymentInfo(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    iban = models.IntegerField(primary_key=True, verbose_name='IBAN')

    def __str__(self):
        return f"""IBAN: {self.iban} with {self.bank}"""
    
class Dependent(Person):

    dependent_of = models.ForeignKey('Employee', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}
    Disability: {self.disability}
    Age: {self.age}"""
    


class Employee(Person):


    # Choice lists
    ## Contract types
    STUDENT_CONTRACT = 'SC'
    INDEFINITE_CONTRACT = 'NDC'
    DEFINITE_CONTRACT = 'DC'
    
    ## Positions
    SUPPORT_EMPLOYEE = 'SE'
    PROJECT_MANAGER = 'PM'
    DEVELOPER = 'D'
    
    # Dependents
    @property
    def no_children(self):
        return 0
    
    @property
    def no_dependents(self):
        return 0
    
    @property
    def no_dependents_disabled(self):
        return 0
    
    @property
    def no_dependents_disabled_100(self):
        return 0
    
    
    positions = [
        (SUPPORT_EMPLOYEE, 'Support employee'),
        (PROJECT_MANAGER, 'Project manager'),
        (DEVELOPER, 'Developer')
    ]
    contract_types = [
        (STUDENT_CONTRACT, 'Student contract'),
        (INDEFINITE_CONTRACT, 'Indefinite contract'),
        (DEFINITE_CONTRACT, 'Definite contract')
    ]
    
    first_employment = models.BooleanField(default=True, verbose_name='First employment')
    employee_since = models.DateField(verbose_name='Employee since')

    # External relations
    payment_info = models.OneToOneField(
        PaymentInfo, on_delete=models.DO_NOTHING, unique=True)
    
    
    contract_type = models.CharField(choices=contract_types, max_length=3, default=INDEFINITE_CONTRACT, verbose_name='Contract type')
    
    position = models.CharField(
        choices=positions, max_length=3, default=SUPPORT_EMPLOYEE, verbose_name='Position')


    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}
    Position: {self.position}"""
