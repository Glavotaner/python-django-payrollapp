from django.db import models

from address.models import EmployeeAddress
from bank.models import Bank


class PaymentInfo(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    iban = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"""IBAN: {self.iban} with {self.bank}"""


class Deductibles(models.Model):
    no_children = models.IntegerField()
    no_dependents = models.IntegerField()
    no_dependents_disabled = models.IntegerField()
    no_dependents_disabled_100 = models.IntegerField()

    def __str__(self):
        return f"""Number of children: {self.no_children}
    Number of dependents: {self.no_dependents}
    Number of disabled dependents: {self.no_dependents_disabled}
    Number of 100% disabled dependents: {self.no_dependents_disabled_100}"""


class Employee(models.Model):

    STUDENT = 'ST'
    FULL_TIME_EMPLOYEE = 'FTE'
    positions = [
        (STUDENT, 'Student'),
        (FULL_TIME_EMPLOYEE, 'Full-time employee')
    ]

    pid = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateTimeField()

    # External relations
    address = models.OneToOneField(EmployeeAddress, on_delete=models.CASCADE)
    payment_info = models.OneToOneField(
        PaymentInfo, on_delete=models.DO_NOTHING, unique=True)
    deductibles = models.OneToOneField(Deductibles, models.CASCADE)

    position = models.CharField(
        choices=positions, max_length=3, default=STUDENT)

    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}"""
