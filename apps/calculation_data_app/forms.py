from typing import List

from django import forms

from apps.calculation_data_app.models import ReimbursementValue, Reimbursement


class ReimbursementValueForm(forms.ModelForm):
    class Meta:
        model = ReimbursementValue
        fields = ['reimbursement', 'amount', 'valid_from']

    valid_reimbursements: List['Reimbursement'] = Reimbursement.objects.filter(retired=False)

    reimbursement = forms.ModelChoiceField(valid_reimbursements)
    amount = forms.FloatField(min_value=0.01)

    valid_from = forms.DateField()
