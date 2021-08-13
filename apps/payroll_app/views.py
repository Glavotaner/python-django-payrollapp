from typing import Any
from django.db.models.query import QuerySet
from apps.payroll_app.models.contribution_amount import ContributionAmount
from apps.payroll_app.models.reimbursement_amount import ReimbursementAmount
from apps.payroll_app.models.payroll import Payroll
from apps.payroll_app.models.labour import Labour
from apps.employee_data_app.employee_app.models.employee import Employee
from apps.payroll_app.forms import PeriodForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from datetime import datetime

from apps.calculation_data_app.models import Reimbursement, HourType, HourFund


def select_period(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        period_form = PeriodForm(request.POST)
        if period_form.is_valid():
            year = period_form.cleaned_data['year']
            month = period_form.cleaned_data['month']
            accounting_date = period_form.cleaned_data['accounting_date']
            page = 'employees' if 'employees' in request.POST else 'data'
            if page == 'employees' and not accounting_date or (any([year, month]) == None):
                return HttpResponseBadRequest()
            if page == 'employees':
                return HttpResponseRedirect(f'{page}_Y{year}M{month}D{accounting_date}')
            if Payroll.objects.filter(year=year, month=month).count() > 0:
                return HttpResponseRedirect(f'payrolls_Y{year}M{month}')

    current_date = datetime.now()
    period_form = PeriodForm(initial={
        'year': current_date.year,
        'month': current_date.month,
        'accounting_date': current_date
    })

    return render(request, 'select_period.html', {'form': period_form})


def process_payroll(request: HttpRequest, **kwargs) -> HttpResponse:
    year = kwargs['year']
    month = kwargs['month']
    accounting_date: str = kwargs['accounting_date']
    accounting_date_parsed = datetime.strptime(accounting_date, '%Y-%m-%d')

    if request.method == 'POST' and request.is_ajax():
        import json
        employees_queryset = None
        action = request.POST.get('action')
        if action == 'selected':
            employees = json.loads(str(request.POST.get('employees')))
            employees = [
                int(employee['id']) for employee in employees if employee['selected']
            ]
            if len(employees) == 0:
                return HttpResponseRedirect(f'employees_Y{year}M{month}D{accounting_date}')
            else: 
                employees_queryset = Employee.objects.filter(pk__in=employees)
        hour_types = json.loads(str(request.POST.get('hour_types')))
        hour_types = [{'id': int(hour_type['id']), 'amount': int(
            hour_type['amount'])} for hour_type in hour_types]

        regular_hours = json.loads(str(request.POST.get('regular_hours')))
        reimbursements = json.loads(str(request.POST.get('reimbursements')))
        reimbursements = [{'id': int(reimbursement['id']), 'amount': float(
            reimbursement['amount'].replace(',', '.'))} for reimbursement in reimbursements]
        labours = Labour.set_labour(int(year), int(
            month), regular_hours, hour_types, employees_queryset)
        payrolls = Payroll.calculate_payrolls(
            accounting_date_parsed, year, month, labours)
        Payroll.calculate_reimbursements(
            accounting_date_parsed, reimbursements, payrolls)
        return HttpResponseRedirect(f'payrolls_Y{year}M{month}')

    eligible_employees = Employee.get_eligible_employees(year, month)
    valid_hour_types = HourType.get_current_hour_types()
    valid_reimbursements = Reimbursement.get_valid_reimbursements(
        accounting_date_parsed
    )
    valid_reimbursements = [
        {
            'reimbursement_name': r.reimbursement_name,
            'reimbursement_id': r.reimbursement_id,
            'amount': '{:.2f}'.format(r.amount).replace('.', ',')
        } for r in valid_reimbursements
    ]
    hours_fund = HourFund.get_hour_fund_for_period(year, month)

    return render(
        request, 'process_payroll.html',
        {
            'employees': eligible_employees,
            'hour_types': valid_hour_types,
            'reimbursements': valid_reimbursements,
            'hour_fund': hours_fund,
        }
    )


def payrolls_processed(request: HttpRequest, **kwargs) -> Any:
    if request.method == 'POST' and request.is_ajax():
        import json
        selected = json.loads(str(request.POST.get('selected')))
        selected = [int(s['id']) for s in selected if s['selected']]
        if len(selected) > 0:
            Payroll.delete_selected_payrolls(selected)
        return HttpResponseRedirect('')

    year = kwargs.pop('year')
    month = kwargs.pop('month')
    payrolls_queryset = Payroll.objects.filter(year=year, month=month)
    employee_data = {
        payroll.payroll_id: {
            'oib': payroll.work_data.employee.oib,
            'name': payroll.work_data.employee.first_name + ' ' + payroll.work_data.employee.last_name
        } for payroll in payrolls_queryset
    }
    if payrolls_queryset:
        payrolls = payrolls_queryset.values()
        for i, payroll in enumerate(payrolls):
            payrolls[i]['employee'] = employee_data[payroll['payroll_id']]
        return render(request, 'processed_payrolls.html', {
            'payrolls': payrolls, 'period': {'year': year, 'month': month}
        })


def payroll_detail(request: HttpRequest, **kwargs):
    payroll_id = kwargs.pop('payroll_id')
    payrolls: QuerySet[Payroll] = Payroll.objects.filter(pk=payroll_id)
    year = payrolls[0].year
    month = payrolls[0].month

    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            Payroll.delete_selected_payrolls([payroll_id])
            if Payroll.objects.filter(year=year, month=month).count() > 0:
                return HttpResponseRedirect(f'payrolls_Y{year}M{month}')
        return HttpResponseRedirect(f'')

    employee_data = {
        'oib': payrolls[0].work_data.employee.oib,
        'name': payrolls[0].work_data.employee.first_name + ' '
        + payrolls[0].work_data.employee.last_name
    }
    payroll = payrolls.values()[0]
    payroll['employee'] = employee_data
    payroll['contributions'] = [{
        'id': c.contribution.contribution_id,
        'name': c.contribution.contribution_name,
        'amount': c.amount,
        'from_pay': c.contribution.from_pay
    }
        for c in ContributionAmount.get_payroll_contribution_amounts(payroll_id)
    ]
    payroll['reimbursements'] = [{
        'id': c.reimbursement.reimbursement_id,
        'name': c.reimbursement.reimbursement_name,
        'amount': c.amount
    }
        for c in ReimbursementAmount.get_payroll_reimbursement_amounts(payroll_id)]
    payroll['total_amount'] = payroll['net_salary'] + payroll['reimbursements_total']
    return render(request, 'payroll_detail.html', {
        'payroll': payroll,
        'contributions_from_pay': [{
            'id': c['id'],
            'name': c['name'],
            'amount': c['amount'],
        } for c in payroll['contributions'] if c['from_pay']],
        'contributions_other': [{
            'id': c['id'],
            'name': c['name'],
            'amount': c['amount'],
        } for c in payroll['contributions'] if not c['from_pay']]
    })
