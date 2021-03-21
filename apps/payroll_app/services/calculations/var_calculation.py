from datetime import date

from apps.calculation_data_app.models import HourFund


def get_accounted_period_id(self):
    return str(self.accounted_period_start)[0:4]


def get_months_hours_fund(accounted_period_start: date):
    acc_period_year = str(accounted_period_start.year)
    acc_period_month = str(accounted_period_start.month)

    monthly_hours_fund = HourFund.objects.raw(
        "SELECT period_id, total_hours FROM calculation_data_app_hourfund WHERE year = %s AND month = %s",
        [acc_period_year, acc_period_month]
    )

    return monthly_hours_fund[0].total_hours
