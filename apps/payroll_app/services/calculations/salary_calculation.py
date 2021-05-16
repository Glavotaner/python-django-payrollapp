from datetime import date

from apps.calculation_data_app.models import HourFund
from apps.payroll_app.models import Labour
from apps.payroll_app.models import WageParameters


class SalaryCalculated:

    def __init__(self, hours: dict, labour_data: Labour, accounting_date: date, wage_parameters: WageParameters):
        self.hours = hours
        self.labour_data: Labour = labour_data
        self.employee = labour_data.employee
        self.accounting_date: date = accounting_date
        self.contracted_salary: float = round(labour_data.employee.signed_contract.total_salary, 2)
        self.wage_parameters = wage_parameters

    @property
    def wage(self) -> float:
        return round(self.contracted_salary * (self.labour_data.regular_hours / self.labour_data.get_hours_fund), 2)
    
    @property
    def extra_hours(self) -> float:
        return self.labour_data.hour_type_amounts

    @property
    def salary(self) -> float:
        if self.labour_data.below_fund:
            pass
