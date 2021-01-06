from apps.employee_data_app.employee_app.models import Employee
from django.utils.translation import gettext_lazy as _


def save_to_employee(self):
    
    emp = Employee.objects.get(pid = self.dependent_of)
    
    if self.disability == 'D':
        emp.no_dependents_disabled += 1
    
    elif self.disability == 'D100':
        emp.no_dependents_disabled_100 += 1
    
    
    if self.child:
        emp.no_children += 1
    
    elif not self.child:
        emp.no_dependents += 1            
    
    emp.save()
    
    
def delete_from_employee(self):
    
    emp = Employee.objects.get(pid = self.dependent_of)
    
    if self.disability == 'D':
        emp.no_dependents_disabled -= 1
    
    elif self.disability == 'D100':
        emp.no_dependents_disabled_100 -= 1
    
    
    if self.child:
        emp.no_children -= 1
    
    elif not self.child:
        emp.no_dependents -= 1
    
    emp.save()
