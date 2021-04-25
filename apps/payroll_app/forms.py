from django.forms import ModelForm

from apps.employee_data_app.employee_app.models import Employee
from apps.payroll_app.models import Labour


class LabourForm(ModelForm):
    class Meta:
        model = Labour
        fields = ('year', 'month', 'regular_hours')


class EmployeesForm(ModelForm):
    class Meta:
        model = Employee
        fields = ('oib', 'first_name', 'last_name')
