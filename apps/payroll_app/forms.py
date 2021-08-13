from django import forms
from django.views import generic
from django.utils.translation import gettext_lazy as _
from apps.employee_data_app.employee_app.models import Employee
from apps.calculation_data_app.models import HourType


class PeriodForm(forms.Form):
    year = forms.IntegerField(label=_('Year'), min_value=2015, max_value=2999)
    month = forms.ChoiceField(label=_('Month'),
                              choices=(
        (1, _('January')),
        (2, _('February')),
        (3, _('March')),
        (4, _('April')),
        (5, _('May')),
        (6, _('June')),
        (7, _('July')),
        (8, _('August')),
        (9, _('September')),
        (10, _('October')),
        (11, _('November')),
        (12, _('December')),
    )
    )
    accounting_date = forms.DateField(
        label=_('Accounting date'), widget=forms.SelectDateWidget)
