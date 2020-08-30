from django.db import models

class Address(models.Model):
    
    class Meta:
        abstract = True
    
    street_name = models.CharField(max_length = 20)
    street_number = models.IntegerField()
    postal_code = models.IntegerField()
    city = models.CharField(max_length = 20)
    

class EmployeeAddress(Address):
    
    def __str__(self):
        return f"""{self.street_name} {self.street_number}, {self.postal_code} {self.city}"""


class BankAddress(Address):
    
    def __str__(self):
        return f"""{self.city}"""
    
    