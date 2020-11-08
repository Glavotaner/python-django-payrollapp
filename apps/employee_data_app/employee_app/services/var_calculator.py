from datetime import date
from datetime import datetime
from dateutil import relativedelta
from apps.employee_data_app.employment_app.models import Contract


def _age(self) -> int:
    today = date.today()
    
    try:
        birthday = self.date_of_birth.replace(year=today.year)

    except ValueError:
        birthday = self.date_of_birth.replace(year=today.year,
                                                month=self.date_of_birth.month + 1, day=1)

    if birthday > today:
        return today.year - self.date_of_birth.year - 1
    else:
        return today.year - self.date_of_birth.year
    

def _employment_duration(self) -> str:
    latest_contract = Contract.objects.filter(pk=2).get()

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
