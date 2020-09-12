from django.db import models

from common.models import Person, Address 
from institutions_data.bank.models import Bank
from employee_data.work_places.models import WorkPlace
from documents_data.documents.models import Contract

    
class Dependent(Person):
    
    DISABLED = 'D'
    DISABLED_100 = 'D100'
    NONE = 'N'
    
    disability = [
        (DISABLED, 'Disabled'),
        (DISABLED_100, '100% disabled'),
        (NONE, 'None')
    ]
    
    # FOREIGN KEYS
    dependent_of = models.ForeignKey('Employee', on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}
    Disability: {self.disability}
    Age: {self.age}"""
    


class Employee(Person, Address):

    # PROPERTIES
    ## DEPENDENTS
    @property
    def no_children(self):
        dep_counter = 0
        
        for dependent in Dependent.objects.filter(dependent_of = self.pid).all():
            if dependent.age <= 16:
                dep_counter += 1
        
        return dep_counter
    
    @property
    def no_dependents(self):
        dep_counter = 0
        
        for dependent in Dependent.objects.filter(dependent_of = self.pid).all():
            if dependent.age > 16:
                dep_counter += 1
        
        return dep_counter
    
    @property
    def no_dependents_disabled(self):
        return 0
    
    @property
    def no_dependents_disabled_100(self):
        return 0
    
 
    iban = models.IntegerField(unique=True, verbose_name='IBAN')
    
    first_employment = models.BooleanField(default=True, verbose_name='First employment')
    
    employee_since = models.DateField(verbose_name='Employee since')


    # FOREIGN KEYS
    work_place = models.ForeignKey(to = WorkPlace, on_delete=models.DO_NOTHING, verbose_name = 'Work place')
    
    contract_type = models.ForeignKey(to = Contract,verbose_name='Contract type', on_delete=models.DO_NOTHING)


    def __str__(self):
        return f"""{self.last_name}, {self.first_name}
    PID: {self.pid}
    No deps: {self.no_dependents}
    No children: {self.no_children}"""
    
    class EmployeeAdmin(admin.ModelAdmin):
        list_display = ('pid', 'disability', 'first_name', 'last_name', 'date_of_birth', 'age')
        
        field_sets = [("Personal", {"fields": (("pid", "first_name", "last_name", "date_of_birth", "age"))})]
