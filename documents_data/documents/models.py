from django.db import models

class Contract(models.Model):
    
    contract_id = models.CharField(max_length = 5, primary_key=True, verbose_name = 'Contract ID')
    contract_type = models.CharField(max_length = 100, verbose_name = 'Contract type', unique = True)
    start_date = models.DateField(verbose_name='Start date')
    expiration_date = models.DateField(verbose_name='Expiration date')
    contract_description = models.CharField(max_length = 255, verbose_name = 'Contract description')
    contract_retired = models.BooleanField(default=False, verbose_name = 'Contract retired')
    
