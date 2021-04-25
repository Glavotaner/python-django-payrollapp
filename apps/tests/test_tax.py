from datetime import date

from django.test import TestCase

from apps.calculation_data_app.models import TaxBracket, TaxModel
from apps.calculation_data_app.services.tax_calculation import TaxCalculated
from apps.tests import load_fixtures
from apps.third_parties_app.models import City


class TaxTest(TestCase):
    fixtures = load_fixtures.load_fixtures()

    def setUp(self) -> None:
        tbr1 = TaxBracket.objects.create(
            amount_from=0,
            amount_to=30000,
            tax_rate=0.20
        )

        tbr2 = TaxBracket.objects.create(
            amount_from=30000.01,
            amount_to=50000,
            tax_rate=0.30
        )

        tbr3 = TaxBracket.objects.create(
            amount_from=50000.01,
            amount_to=None,
            tax_rate=0.40
        )

        tbr1.save()
        tbr2.save()
        tbr3.save()

        tax_model = TaxModel.objects.create(
            valid_from=date.today(),
        )

        tax_model.save()

        tax_model.tax_brackets.add(tbr1, tbr2, tbr3)

    def test_lowest(self):
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        income: float = 10000
        tax_bracket: TaxBracket = tax_model.get_tax_bracket(income)

        tax_rate: float = tax_bracket.tax_rate

        self.assertEqual(tax_rate, 0.20)

    def test_highest(self):
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        income: float = 30000.02
        tax_bracket: TaxBracket = tax_model.get_tax_bracket(income)

        tax_rate: float = tax_bracket.tax_rate

        self.assertEqual(tax_rate, 0.30)

    def test_low_income_tax(self):
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        calculated_tax: TaxCalculated = TaxCalculated(tax_model, 5000, 0)

        self.assertEqual(
            calculated_tax.income_tax,
            1000
        )

    def test_hi_income_tax(self):
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        calculated_tax: TaxCalculated = TaxCalculated(tax_model, 60000, 0)

        self.assertEqual(
            calculated_tax.income_tax,
            (4000 + 6000 + 6000)
        )

    def test_zero(self):
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        calculated_tax: TaxCalculated = TaxCalculated(tax_model, 0, 0)

        self.assertEqual(
            calculated_tax.income_tax,
            0
        )

    def test_negative(self):
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        calculated_tax: TaxCalculated = TaxCalculated(tax_model, -2000, 0)

        self.assertEqual(
            calculated_tax.income_tax,
            0
        )

    def test_multiple(self):
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        calculated_tax: TaxCalculated = TaxCalculated(tax_model, 200000, 0)

        self.assertEqual(
            calculated_tax.income_tax,
            (60000 + 6000 + 6000)
        )

    def test_city_tax_13(self):
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        calculated_tax: TaxCalculated = TaxCalculated(tax_model, 5000, City.get_city_tax_rate(joppd='03123'))

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
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        calculated_tax: TaxCalculated = TaxCalculated(tax_model, 5000, City.get_city_tax_rate(joppd='03166'))

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
        tax_model: TaxModel = TaxModel.get_valid_tax_model(date.today())

        calculated_tax: TaxCalculated = TaxCalculated(tax_model, 5000, 0)

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
