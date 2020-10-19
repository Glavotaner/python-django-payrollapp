def _wage(self):
    return round(float(self.employee.signed_contract.position.salary) / self.months_hours_fund, 2)


def _overtime_hours_gross(self):
    return round(self.work_data.overtime_hours * self.wage + (self.wage * 0.5), 2)


def _special_hours_gross(self):
    return round(self.work_data.special_hours * self.wage + (self.wage * 0.6), 2)


def _gross_salary(self):
    if self.work_data.regular_hours < self.months_hours_fund:
        return round(self.wage * self.work_data.regular_hours, 2)

    return round(self.employee.signed_contract.position.salary, 2)