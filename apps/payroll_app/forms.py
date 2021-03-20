from django.forms import ModelForm

from .models import Payroll


class PayrollForm(ModelForm):
    class Meta:
        model = Payroll
        fields = ['accounted_period_start', 'accounted_period_end']
