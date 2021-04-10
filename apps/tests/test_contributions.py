from django.test import TestCase

from apps.calculation_data_app.models import ContributionsModel
from apps.calculation_data_app.services.contributions_calculation import ContributionsModelCalculated, \
    get_contributions_model
from apps.tests import load_fixtures


class TestContributions(TestCase):
    fixtures = load_fixtures.load_fixtures()

    def test_regular(self):
        model: ContributionsModel = get_contributions_model('REG')
        contributions_base: float = 4000

        assertion: dict = {'pension_fund_gen': 600, 'pension_fund_ind': 200, 'health_insurance': 660}

        calculated: ContributionsModelCalculated = ContributionsModelCalculated(contributions_base, model)

        self.assertEqual(
            assertion['pension_fund_gen'], calculated.pension_fund_gen
        )

        self.assertEqual(
            assertion['pension_fund_ind'], calculated.pension_fund_ind
        )

        self.assertEqual(
            assertion['health_insurance'], calculated.health_insurance
        )

    def test_regular_below_min(self):
        model: ContributionsModel = get_contributions_model('REG')
        contributions_base: float = 3000

        assertion: dict = {'pension_fund_gen': 523.32, 'pension_fund_ind': 174.44, 'health_insurance': 575.65}

        calculated: ContributionsModelCalculated = ContributionsModelCalculated(contributions_base, model)

        self.assertEqual(
            assertion['pension_fund_gen'], calculated.pension_fund_gen
        )

        self.assertEqual(
            assertion['pension_fund_ind'], calculated.pension_fund_ind
        )

        self.assertEqual(
            assertion['health_insurance'], calculated.health_insurance
        )

    def test_regular_above_max(self):
        model: ContributionsModel = get_contributions_model('REG')
        contributions_base: float = 55090

        assertion: dict = {'pension_fund_gen': 8262.9, 'pension_fund_ind': 2754.3, 'health_insurance': 9089.19}

        calculated: ContributionsModelCalculated = ContributionsModelCalculated(contributions_base, model)

        self.assertEqual(
            assertion['pension_fund_gen'], calculated.pension_fund_gen
        )

        self.assertEqual(
            assertion['pension_fund_ind'], calculated.pension_fund_ind
        )

        self.assertEqual(
            assertion['health_insurance'], calculated.health_insurance
        )

    def test_y30(self):
        model: ContributionsModel = get_contributions_model('Y30')
        contributions_base: float = 4000

        assertion: dict = {'pension_fund_gen': 600, 'pension_fund_ind': 200, 'health_insurance': 0}

        calculated: ContributionsModelCalculated = ContributionsModelCalculated(contributions_base, model)

        self.assertEqual(
            assertion['pension_fund_gen'], calculated.pension_fund_gen
        )

        self.assertEqual(
            assertion['pension_fund_ind'], calculated.pension_fund_ind
        )

        self.assertEqual(
            assertion['health_insurance'], calculated.health_insurance
        )
