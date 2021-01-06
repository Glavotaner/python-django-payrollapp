from datetime import date
from datetime import datetime
from dateutil import relativedelta


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
    today = datetime.today()

    dif = relativedelta.relativedelta(today, self.signed_contract.sign_date)

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
