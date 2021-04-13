from typing import List


def load_fixtures() -> List[str]:
    return [
        'apps/calculation_data_app/fixtures/deductibles_model_fixtures.json',

        'apps/calculation_data_app/fixtures/contribution_fixtures.json',
        'apps/calculation_data_app/fixtures/contribution_rate_fixtures.json',
        'apps/calculation_data_app/fixtures/contributions_model_fixtures.json',

        'apps/calculation_data_app/fixtures/hour_fund_fixtures.json',

        'apps/calculation_data_app/fixtures/hour_type_fixtures.json',
        'apps/calculation_data_app/fixtures/hour_type_coef_fixtures.json',
        
        'apps/calculation_data_app/fixtures/reimbursement_fixtures.json',
        'apps/calculation_data_app/fixtures/reimbursement_value_fixtures.json',

        'apps/calculation_data_app/fixtures/tax_break_fixtures.json',

        'apps/calculation_data_app/fixtures/tax_bracket_fixtures.json',
        'apps/calculation_data_app/fixtures/tax_model_fixtures.json',

        'apps/employee_data_app/employment_app/fixtures/position_fixtures.json',
        'apps/employee_data_app/employment_app/fixtures/contract_type_fixtures.json',

        'apps/payroll_app/fixtures/wage_parameters_fixtures.json',

        'apps/third_parties_app/fixtures/bank_fixtures.json',
        'apps/third_parties_app/fixtures/city_fixtures.json',
    ]
