from typing import List

from apps.calculation_data_app.models import TaxBracket, TaxModel, TaxBreak


class TaxCalculated:
    def __init__(self,
                 tax_model: TaxModel,
                 tax_base: float,
                 city_tax_rate: float,
                 hrvi: float = None,
                 tax_breaks: List[TaxBreak] = None):
        self.city_tax_rate = city_tax_rate
        self.tax_base = tax_base
        self.tax_model = tax_model
        self.hrvi = hrvi
        self.tax_breaks = tax_breaks

    @property
    def income_tax(self) -> float:

        if self.tax_base <= 0:
            return 0

        reduced_income: float = self.tax_base
        income_tax: float = 0

        taxable: float = 0

        # calculate through tax brackets
        while True:
            highest_bracket: TaxBracket = self.tax_model.get_tax_bracket(
                reduced_income)

            if not highest_bracket.amount_to:
                taxable = (self.tax_base - highest_bracket.amount_from) + 0.01
            elif highest_bracket.amount_to and self.tax_base >= highest_bracket.amount_to:
                taxable = (highest_bracket.amount_to -
                           highest_bracket.amount_from) + 0.01

            if (highest_bracket.amount_to
                and self.tax_base < highest_bracket.amount_to) \
                    and highest_bracket.amount_from <= 0:
                taxable = self.tax_base

            reduced_income -= taxable

            income_tax += taxable * highest_bracket.tax_rate

            if highest_bracket.amount_from <= 0:
                break

        return round(income_tax, 2)

    @property
    def tax_break_amount(self):

        hrvi: float = self.hrvi if self.hrvi else 0
        tax_breaks: List[TaxBreak] = self.tax_breaks if self.tax_breaks else []

        deduction: float = hrvi + \
            sum([tax_break.rate for tax_break in tax_breaks])

        total_tax_break: float = round(
            ((deduction * self.income_tax) * 100), 2)

        return total_tax_break if total_tax_break > 0 else 0

    @property
    def city_tax(self) -> float:
        if self.income_tax == 0:
            return 0
        return round(self.income_tax * (self.city_tax_rate / 100), 2)

    @property
    def total_tax(self):
        return round(
            (self.income_tax - self.tax_break_amount) + self.city_tax, 2)
