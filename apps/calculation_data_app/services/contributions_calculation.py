from ..models import ContributionsModel


def get_contributions_model(model_mark: str) -> ContributionsModel:
    return ContributionsModel.objects.get(model_mark=model_mark)


class ContributionsModelCalculated:

    def __init__(self, contributions_base: float, contributions_model):
        if contributions_base <= contributions_model.min_base:
            self.contributions_base = contributions_model.min_base
        elif contributions_base >= contributions_model.max_base:
            self.contributions_base = contributions_model.max_base
        else:
            self.contributions_base = contributions_base

        self.contributions_model = contributions_model

    @property
    def pension_fund_gen(self) -> float:
        if self.contributions_model.pension_fund_gen and self.contributions_model.pension_fund_gen > 0:
            return round(self.contributions_base * (self.contributions_model.pension_fund_gen / 100), 2)
        else:
            return 0

    @property
    def pension_fund_ind(self) -> float:
        if self.contributions_model.pension_fund_ind and self.contributions_model.pension_fund_ind > 0:
            return round(self.contributions_base * (self.contributions_model.pension_fund_ind / 100), 2)
        else:
            return 0

    @property
    def health_insurance(self) -> float:
        if self.contributions_model.health_insurance and self.contributions_model.health_insurance > 0:
            return round(self.contributions_base * (self.contributions_model.health_insurance / 100), 2)
        else:
            return 0
