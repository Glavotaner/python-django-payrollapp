class ContributionsModelCalculated:

    def __init__(self, wage_parameters, labour_data, contributions_base):
        self.wage_parameters = wage_parameters
        self.labour_data = labour_data

        hours_fund: int = self.labour_data.get_hours_fund()

    @property
    def return_calculated_contributions(self) -> dict:
