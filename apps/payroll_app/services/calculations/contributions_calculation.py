def _contributions_base(self):
   if self.work_data.regular_hours < self.months_hours_fund:
            proportional_min_base = (self.employee.contibutions_model.pension_fund_min_base /
                                     self.months_hours_fund) * self.labour_data.total_hours

        if self.gross_salary < proportional_min_base:
            return proportional_min_base

        elif self.gross_salary > proportional_min_base:
            return self.gross_salary

    elif self.gross_salary < self.employee.contributions_model.pension_fund_min_base:
        return self.employee.contributions_model.pension_fund_min_base

    return self.gross_salary 


def _health_insurance_amount(self) -> float:
        return round(self.gross_salary * self.employee.contributions_model.health_insurance, 2)
    

def _pension_fund_gen_amount(self) -> float:
    return round(self.gross_salary * self.employee.contributions_model.pension_fund_gen, 2)


def _pension_fund_ind_amount(self) -> float:
    return round(self.gross_salary * self.employee.contributions_model.pension_fund_ind, 2)


def _pension_fund_total(pension_fund_gen_amount: float, pension_fund_ind_amount: float) -> float:
    return round(pension_fund_gen_amount + pension_fund_ind_amount, 2)