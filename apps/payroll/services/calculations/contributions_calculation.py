def calculate_health_insurance_amount(gross_salary: object, employee: object) -> float:
        return round(gross_salary * employee.contributions_model.health_insurance, 2)
    

def calculate_pension_fund_gen_amount(gross_salary: object, employee: object) -> float:
    return round(gross_salary * employee.contributions_model.pension_fund_gen, 2)


def calculate_pension_fund_ind_amount(gross_salary: object, employee: object) -> float:
    return round(gross_salary * employee.contributions_model.pension_fund_ind, 2)


def calculate_pension_fund_total(pension_fund_gen_amount: float, pension_fund_ind_amount: float) -> float:
    return round(pension_fund_gen_amount + pension_fund_ind_amount, 2)