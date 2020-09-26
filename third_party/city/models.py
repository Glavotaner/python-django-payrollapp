from django.db import models


class City(models.Model):
    
    

    
    iban = models.CharField(max_length = 10, verbose_name = 'IBAN')
    joppd = models.CharField(max_length = 5, verbose_name = 'JOPPD', primary_key=True)
    city_name = models.CharField(max_length = 50, verbose_name = 'City name')
    postal_code = models.IntegerField(verbose_name = 'Postal code')
    tax_rate = models.FloatField(verbose_name='Tax rate', default=0.00)
    tax_break = models.FloatField(verbose_name = 'Tax break', default=0.00)
    
    
    def __str__(self):
        return f"""{self.city_name}"""
    
