from django.db.models import Q

from apps.calculation_data_app.models import TaxBracket
from apps.third_parties_app.models import City


def get_tax_bracket(income: float) -> TaxBracket:
    return TaxBracket.objects.filter(Q(tax_from__lte=income), (Q(tax_to__gte=income) |
                                                               Q(tax_to__isnull=True))).order_by('tax_from').get()


def get_city_tax_rate(joppd: str) -> float:
    return City.objects.get(pk=joppd).tax_rate


class TaxCalculated:
    def __init__(self, tax_base: float, city_tax_rate: float = None):
        self.city_tax_rate = city_tax_rate
        self.tax_base = tax_base

    @property
    def income_tax(self) -> float:

        if self.tax_base <= 0:
            return 0

        reduced_income: float = self.tax_base
        income_tax: float = 0

        taxable: float = 0

        while True:
            highest_bracket: TaxBracket = get_tax_bracket(reduced_income)

            if not highest_bracket.tax_to:
                taxable = (self.tax_base - highest_bracket.tax_from) + 0.01
            elif highest_bracket.tax_to and self.tax_base >= highest_bracket.tax_to:
                taxable = (highest_bracket.tax_to - highest_bracket.tax_from) + 0.01

            if (highest_bracket.tax_to and self.tax_base < highest_bracket.tax_to) and highest_bracket.tax_from <= 0:
                taxable = self.tax_base

            reduced_income -= taxable

            income_tax += taxable * highest_bracket.tax_rate

            if highest_bracket.tax_from <= 0:
                break

        return round(income_tax, 2)

    @property
    def city_tax(self) -> float:
        if self.income_tax == 0:
            return 0

        return round(self.income_tax * (self.city_tax_rate / 100), 2) if self.city_tax_rate else 0

    @property
    def total_tax(self):
        return self.income_tax + self.city_tax
