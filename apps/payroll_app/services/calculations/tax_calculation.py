def _income(self):
    if self.gross_salary - self.pension_fund_total < self.employee.contributions_model.pension_fund_min_base:
        return round(self.employee.contributions_model.pension_fund_min_base, 2)

    return round(self.gross_salary - self.pension_fund_total, 2) 


def _tax_base(self):
    if self.deductibles > self.income:
        return 0

    return round(self.income - self.deductibles, 2)


def _income_tax_amount(self) -> float:

    if self.tax_base > self.current_tax_model.tax_bracket:
        hi_tax_base = self.tax_base - \
            self.current_tax_model.tax_bracket

        income_tax = (self.current_tax_model.tax_bracket *
                      self.current_tax_model.lo_tax_rate) + \
            (hi_tax_base * self.current_tax_model.hi_tax_rate)

    else:
        income_tax = self.tax_base * \
            self.current_tax_model.lo_tax_rate

    return round(income_tax, 2)


def _city_tax_amount(self) -> float:
    return round(self.income_tax_amount * (self.employee.city.tax_rate -
                                      self.employee.city.tax_break), 2)


def _tax_amount(self) -> float:
    return round(self.income_tax_amount + self.city_tax_amount, 2)
