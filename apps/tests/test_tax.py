from django.test import TestCase

from apps.calculation_data_app.models import TaxBracket
from apps.calculation_data_app.services.tax_calculation import get_tax_bracket, get_city_tax_rate, TaxCalculated
from apps.tests import load_fixtures


class TaxTest(TestCase):
    fixtures = load_fixtures.load_fixtures()

    def setUp(self) -> None:
        TaxBracket.objects.create(
            tax_from=0,
            tax_to=30000,
            tax_rate=0.20
        ).save()

        TaxBracket.objects.create(
            tax_from=30000.01,
            tax_to=50000,
            tax_rate=0.30
        ).save()

        TaxBracket.objects.create(
            tax_from=50000.01,
            tax_to=None,
            tax_rate=0.40
        ).save()

    def test_lowest(self):
        income: float = 10000
        tax_model: TaxBracket = get_tax_bracket(income)

        tax_rate: float = tax_model.tax_rate

        self.assertEqual(tax_rate, 0.20)

    def test_highest(self):
        income: float = 30000.02
        tax_model: TaxBracket = get_tax_bracket(income)

        tax_rate: float = tax_model.tax_rate

        self.assertEqual(tax_rate, 0.30)

    def test_low_income_tax(self):
        calculated_tax: TaxCalculated = TaxCalculated(5000)

        self.assertEqual(
            calculated_tax.income_tax,
            1000
        )

    def test_hi_income_tax(self):
        calculated_tax: TaxCalculated = TaxCalculated(60000)

        self.assertEqual(
            calculated_tax.income_tax,
            (4000 + 6000 + 6000)
        )

    def test_zero(self):
        calculated_tax: TaxCalculated = TaxCalculated(0)

        self.assertEqual(
            calculated_tax.income_tax,
            0
        )

    def test_negative(self):
        calculated_tax: TaxCalculated = TaxCalculated(-2000)

        self.assertEqual(
            calculated_tax.income_tax,
            0
        )

    def test_multiple(self):
        calculated_tax: TaxCalculated = TaxCalculated(200000)

        self.assertEqual(
            calculated_tax.income_tax,
            (60000 + 6000 + 6000)
        )

    def test_city_tax_13(self):
        calculated_tax: TaxCalculated = TaxCalculated(5000, get_city_tax_rate('03123'))

        self.assertEqual(
            calculated_tax.income_tax,
            1000
        )
        self.assertEqual(
            calculated_tax.city_tax,
            130
        )
        self.assertEqual(
            calculated_tax.total_tax,
            1130
        )

    def test_city_tax_0(self):
        calculated_tax: TaxCalculated = TaxCalculated(5000, get_city_tax_rate('03166'))

        self.assertEqual(
            calculated_tax.income_tax,
            1000
        )
        self.assertEqual(
            calculated_tax.city_tax,
            0
        )
        self.assertEqual(
            calculated_tax.total_tax,
            1000
        )

    def test_city_tax_none(self):
        calculated_tax: TaxCalculated = TaxCalculated(5000)

        self.assertEqual(
            calculated_tax.income_tax,
            1000
        )
        self.assertEqual(
            calculated_tax.city_tax,
            0
        )
        self.assertEqual(
            calculated_tax.total_tax,
            1000
        )
