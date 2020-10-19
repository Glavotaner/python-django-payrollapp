from datetime import datetime
from dateutil import relativedelta
from apps.employee_data_app.employment_app.models import Contract


def _employment_duration(self):
    latest_contract = Contract.objects.filter(
        employee=self.pid).order_by('-sign_date')[0]

    today = datetime.today()

    dif = relativedelta.relativedelta(today, latest_contract.sign_date)

    dm = str(dif.months)
    dy = str(dif.years)
    dd = str(dif.days)

    if len(dy) < 2:
        dy = str('0' + dy)
    if len(dm) < 2:
        dm = str('0' + dm)
    if len(dd) < 2:
        dd = str('0' + dd)

    return f"{dy}{dm}{dd}"
