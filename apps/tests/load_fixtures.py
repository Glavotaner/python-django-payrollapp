from typing import List


def load_fixtures() -> List[str]:
    return [
        'apps/calculation_data_app/fixtures/deductibles_model_fixtures.json',
        'apps/calculation_data_app/fixtures/contributions_model_fixtures.json',
        'apps/third_parties_app/fixtures/bank_fixtures.json',
        'apps/third_parties_app/fixtures/city_fixtures.json',
        'apps/employee_data_app/employment_app/fixtures/position_fixtures.json',
        'apps/employee_data_app/employment_app/fixtures/contract_type_fixtures.json',
    ]
