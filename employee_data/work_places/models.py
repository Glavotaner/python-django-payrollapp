from django.db import models


class WorkPlace(models.Model):
    
    
    work_place_name = models.CharField(max_length = 50, verbose_name="Work place name")
    gross_salary = models.DecimalField(verbose_name="Gross salary", decimal_places=2, max_digits=6) 
