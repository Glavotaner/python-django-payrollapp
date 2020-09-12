from django.db import models


class City(models.Model):
    
    
    iban = models.CharField(max_length = 10, verbose_name = 'IBAN')
    city = models.CharField(max_length = 50, verbose_name = 'City name')
    tax_rate = models.DecimalField(verbose_name='Tax rate', decimal_places=2, max_digits=4)
    
    
    def __str__(self):
        return f"""{self.city}"""
    
