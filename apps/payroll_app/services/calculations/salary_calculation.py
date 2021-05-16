from apps.calculation_data_app.models import HourTypeCoef
from datetime import date

from apps.payroll_app.models import Labour
from apps.payroll_app.models import WageParameters


class SalaryCalculated:

    def __init__(self, labour_data: Labour, accounting_date: date, wage_parameters: WageParameters):
        self.labour_data: Labour = labour_data
        self.accounting_date: date = accounting_date
        self.contracted_salary: float = round(
            labour_data.employee.signed_contract.total_salary,
            2)
        self.wage_parameters = wage_parameters

    @property
    def wage_total(self) -> float:
        return round(
            self.contracted_salary / self.labour_data.get_hours_fund,
            2)

    @property
    def wage_real(self) -> float:
        return round(self.contracted_salary * (self.labour_data.regular_hours / self.labour_data.get_hours_fund), 2)

    @property
    def extra_hours_salary(self) -> float:
        return round(sum(
            [(hour_type_amount.amount * self.wage_total) *
             HourTypeCoef.get_valid_hour_type_coef(
                hour_type_amount.hour_type,
                self.accounting_date)
                for hour_type_amount in self.labour_data.hour_type_amounts]), 2)

    @property
    def regular_hours_salary(self) -> float:
        regular_salary: float = self.wage_real * self.labour_data.regular_hours
        if self.wage_parameters.below_min_wage(regular_salary):
            return round(self.wage_parameters.min_wage, 2)
        return round(regular_salary, 2)

    @property
    def total_salary(self) -> float:
        return self.regular_hours_salary + self.extra_hours_salary
