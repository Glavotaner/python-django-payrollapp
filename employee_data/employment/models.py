from django.db import models


class Position(models.Model):

    
    position_id = models.IntegerField(primary_key=True, verbose_name='Position ID')
    position_name = models.CharField(max_length=30, verbose_name = 'Position name', unique=True)
    salary = models.FloatField(verbose_name = 'Salary') 
    
    
    def __str__(self):
        return self.position_name
    

class Contract(models.Model):
    
    contract_type = models.CharField(max_length=30, verbose_name = 'Contract type')
    
    
    def __str__(self):
        return self.contract_type
    
    
class SignedContract(models.Model):
    
    contract_type = models.ForeignKey(Contract, verbose_name = 'Contract type', on_delete=models.DO_NOTHING)
    position = models.ForeignKey(Position, verbose_name = 'Position', on_delete = models.DO_NOTHING)
    sign_date = models.DateField(verbose_name = 'Sign date')
    expiration_date = models.DateField(verbose_name = 'Expiration date', blank=True, null=True)
    
    
    def __str__(self):
        
        if self.expiration_date:
            return f"{self.contract_type.contract_type} contract | Signed: {self.sign_date} - Expires on: {self.expiration_date}"
        
        return f"{self.contract_type.contract_type} contract | Signed: {self.sign_date}"