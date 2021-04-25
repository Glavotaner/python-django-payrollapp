from datetime import date

from apps.calculation_data_app.models import HourFund
from apps.payroll_app.models import Labour
from apps.payroll_app.models import WageParameters


class SalaryCalculated:

    def __init__(self, hours: dict, labour_data: Labour, accounting_date: date, wage_parameters: WageParameters):
        self.hours = hours
        self.labour_data: Labour = labour_data
        self.accounting_date: date = accounting_date
        self.contracted_salary: float = round(labour_data.employee.signed_contract.position.salary *
                                              labour_data.employee.signed_contract.multiplier, 2)
        self.wage_parameters = wage_parameters

    @property
    def salary(self) -> float:

        if self.hours == 'regular_hours':

            hours_fund: int = HourFund.get_hour_fund_for_period(
                self.labour_data.year, self.labour_data.month
            )

            if self.labour_data.regular_hours < hours_fund:
                return round((self.labour_data.regular_hours / hours_fund) * self.contracted_salary, 2)

            return round(self.contracted_salary, 2)

        else:

            if self.hours.get(self.hours) <= 0:
                return 0

            # return round(self.hours.get(self.hours) * self.wage_parameters.work_type_coefs.get(self.hours), 2)
