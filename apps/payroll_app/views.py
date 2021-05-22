from datetime import date
from typing import Any, Dict, List

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, ListView

from apps.calculation_data_app.models import HourType, HourFund, Reimbursement
from apps.payroll_app.models import Labour
from .forms import LabourForm


class Table(TemplateView):
    template_name = 'set_labour.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        labours = Labour.objects.all()
        res: List[Dict] = []

        # hours_type_names = [{'id': hour.hour_type_id, 'name': hour.hour_type_name} for hour in
        # labours.get(pk=16).hour_type_amounts]

        for labour in labours:
            res.append({
                'labour_data': labour,
                'hours_data': labour.hour_type_amounts})

        ctx = super(Table, self).get_context_data(**kwargs)

        if len(res) > 0:
            ctx['data'] = [lbr.year for lbr in res[0]]
        else:
            ctx['data'] = None

        ctx['headers'] = ['Year', 'Month', 'Regular hours']
        # ctx['headers'].extend([hour['name'] for hour in hours_type_names])

        return ctx


class EligibleEmployees(ListView):
    pass

    # queryset = Employee.get_eligible_employees(year=year, month=month)


def set_labour(request):
    hour_types = HourType.get_current_hour_types()

    if request.method == 'POST':
        form = LabourForm(request.POST, request.FILES)

        hours = []

        for _id in [hour_type.html_id for hour_type in hour_types]:
            hour_type_id: int = int(_id[:_id.find('id')])
            amount: int = int(request.POST[_id])

            if amount < 0:
                raise ValidationError(_('Hours amount cannot be less than 0!'))

            hours.append({'id': hour_type_id, 'amount': amount})

            if form.is_valid():
                Labour.set_labour(form.cleaned_data['year'],
                                  form.cleaned_data['month'],
                                  form.cleaned_data['regular_hours'],
                                  hours)

    else:
        form = LabourForm()

        form.fields['year'].initial = date.today().year
        form.fields['month'].initial = date.today().month
        form.fields['regular_hours'].initial = HourFund.get_hour_fund_for_period(
            year=date.today().year,
            month=date.today().month
        )

    return render(request, 'set_labour.html', {'form': form, 'hour_types': hour_types})


def set_reimbursements(request):
    reimbursements = Reimbursement.get_valid_reimbursements()

    if request.method == 'POST':
        reimbursements_list = []

        for _id in [reimbursement.html_id for reimbursement in reimbursements]:
            reimbursement_id: int = int(_id[:_id.find('id')])
            amount: float = int(request.POST[_id])

            if amount < 0:
                raise ValidationError(_('Reimbursement amount cannot be less than 0!'))

            reimbursements_list.append({'id': reimbursement_id, 'amount': amount})
