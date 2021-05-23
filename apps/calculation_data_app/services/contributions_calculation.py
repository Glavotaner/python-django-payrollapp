from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from apps.payroll_app.models import Labour, WageParameters, ContributionAmount, Payroll
    from apps.calculation_data_app.models import ContributionsModel, ContributionRate


class ContributionsModelCalculated:

    def __init__(self,
                 wage_parameters: 'WageParameters',
                 contributions_model: 'ContributionsModel',
                 labour_data: 'Labour',
                 contributions_base: float,
                 payroll: 'Payroll' = None):
        self.wage_parameters = wage_parameters
        self.contributions_model = contributions_model
        self.labour_data = labour_data
        self.payroll = payroll
        self.contributions_base = contributions_base

    @property
    def calculated_contributions_base(self) -> float:
        if not self.labour_data.below_fund:
            if self.contributions_base < self.wage_parameters.min_base:
                return self.wage_parameters.min_base

            return self.contributions_base

        proportional_base: float = (
            self.contributions_base / self.labour_data.get_hours_fund
        ) * self.labour_data.regular_hours

        proportional_min_base: float = (
            self.wage_parameters.min_base / self.labour_data.get_hours_fund
        ) * self.labour_data.regular_hours

        return round(proportional_min_base if proportional_base < proportional_min_base else proportional_base, 2)

    @property
    def calculated_contributions_from_pay(self) -> float:
        return round(
            sum([
                self.contributions_base * (contribution.rate / 100)
                for contribution in self.contributions_model.get_contribs_from_pay
            ]), 2)

    @property
    def calculated_contributions_other(self) -> float:
        return round(
            sum([
                self.contributions_base * (contribution.rate / 100)
                for contribution in self.contributions_model.get_contribs_other
            ]), 2)

    def save_calculated_contributions(self) -> None:
        contributions: List['ContributionRate'] = self.contributions_model.contributions

        for contribution in contributions:
            ContributionAmount.objects.create(
                contribution=contribution.contribution,
                payroll=self.payroll,
                amount=self.calculated_contributions_base * contribution.rate
            ).save()
