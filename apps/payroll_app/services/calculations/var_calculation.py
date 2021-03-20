from apps.calculation_data_app.models import HourFund


def get_accounted_period_id(self):
    return str(self.accounted_period_start)[0:4]


def get_months_hours_fund(self):
    acc_period_year = str(self.accounted_period_start)[0:4]
    acc_period_month = str(self.accounted_period_start)[5:7]

    monthly_hours_fund_id = HourFund.objects.get(year=acc_period_year, month=acc_period_month)

    return monthly_hours_fund_id.total_hours
