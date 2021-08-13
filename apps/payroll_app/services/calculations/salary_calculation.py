from apps.calculation_data_app.models import HourTypeCoef
from datetime import date

from apps.payroll_app.models import Labour


class SalaryCalculated:

    def __init__(self, labour_data: Labour, accounting_date: date, wage_parameters):
        self.labour_data: Labour = labour_data
        self.accounting_date: date = accounting_date
        self.contracted_salary: float = (
            labour_data.employee.signed_contract.total_salary
            )
        self.wage_parameters = wage_parameters
        print('contracted', self.contracted_salary)

    @property
    def wage_total(self) -> float:
        return (
            self.contracted_salary / self.labour_data.get_hours_fund
            )

    @property
    def wage_real(self) -> float:
        return (
            (self.contracted_salary / self.labour_data.get_hours_fund) *
            (self.labour_data.regular_hours / self.labour_data.get_hours_fund)
            )

    @property
    def extra_hours_salary(self) -> float:
        return sum(
            [(hour_type_amount.amount * self.wage_total) *
             HourTypeCoef.get_valid_hour_type_coef(
                hour_type_amount.hour_type,
                self.accounting_date)
                for hour_type_amount in self.labour_data.hour_type_amounts])

    @property
    def regular_hours_salary(self) -> float:
        regular_salary: float = self.wage_real * self.labour_data.regular_hours
        if self.wage_parameters.get_proportional_min_wage(self.labour_data) \
                > regular_salary:
            return (
                self.wage_parameters
                    .get_proportional_min_wage(self.labour_data)
            )
        return regular_salary

    @property
    def total_salary(self) -> float:
        return round(self.regular_hours_salary + self.extra_hours_salary, 2)

    @property
    def contributions_base(self) -> float:
        if self.wage_parameters.get_proportional_min_base(self.labour_data) \
                > self.total_salary:
            return round(
                self.wage_parameters.get_proportional_min_base(self.labour_data), 2)
        return round(self.total_salary, 2)
