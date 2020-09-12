from django.db import models
from django.contrib import admin


from datetime import timezone, date
from institutions_data.city.models import City

# Create your models here.


class AbstractAddress(models.Model):
    
    class Meta:
        abstract = True
    
    street_name = models.CharField(max_length = 20, verbose_name='Street name')
    street_number = models.IntegerField(verbose_name='Street number')
    postal_code = models.IntegerField(verbose_name='Postal code')
    city = models.ForeignKey(City, verbose_name='City name', on_delete=models.DO_NOTHING)
    

class Address(AbstractAddress):
    
    class Meta:
        verbose_name_plural = "Addresses"
    
    def __str__(self):
        return f"""{self.street_name} {self.street_number}, {self.postal_code} {self.city}"""

   

class PersonModel(models.Model):
    
    class Meta:
        abstract = True
        
    
    DISABLED = 'D'
    DISABLED_100 = 'D100'
    NONE = 'N'
    
    disability = [
        (DISABLED, 'Disabled'),
        (DISABLED_100, '100% disabled'),
        (NONE, 'None')
    ]
    
    pid = models.CharField(primary_key = True, max_length = 11, verbose_name='PID')
    first_name = models.CharField(max_length = 30, verbose_name='First name')
    last_name = models.CharField(max_length = 20, verbose_name='Last name')
    date_of_birth = models.DateField(verbose_name='Date of birth')
    
    @property
    def age(self):
        today = date.today() 
        try:  
            birthday = self.date_of_birth.replace(year = today.year) 
    
        # raised when birth date is February 29 
        # and the current year is not a leap year 
        except ValueError:  
            birthday = self.date_of_birth.replace(year = today.year, 
                    month = self.date_of_birth.month + 1, day = 1) 
    
        if birthday > today: 
            return today.year - self.date_of_birth.year - 1
        else: 
            return today.year - self.date_of_birth.year 
        
    disability = models.CharField(choices=disability, max_length=4, verbose_name='Disability', default = NONE)
    
    
class Person(PersonModel):
    
    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}"""
    

class PersonAdmin(admin.ModelAdmin):
    list_display = ('pid', 'disability', 'first_name', 'last_name', 'date_of_birth', 'age')
    
    field_sets = [("Personal", {"fields": (("pid", "first_name", "last_name", "date_of_birth", "age"))})]
    
    