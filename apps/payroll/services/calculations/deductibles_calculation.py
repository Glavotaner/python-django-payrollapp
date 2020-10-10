
def calculate_personal_deductible_amount(current_deductibles_model: object):
    return round(current_deductibles_model.base_deductible * \
        current_deductibles_model.personal_deductible_coef, 2)


def calculate_dependents_children(current_deductibles_model: object, employee: object):
    child_coefs = [0.7, 1.0, 1.4, 1.9, 2.5, 3.2, 4.0, 4.9, 5.9, 7]

    if 0 < employee.no_children < 10:
        return round(child_coefs[employee.no_children - 1] * \
            current_deductibles_model.base_deductible, 2)
    elif employee.no_children <= 0:
        return 0
    else:
        return round(((employee.no_children - 9) * 1.1 + 7) * \
            current_deductibles_model.base_deductible, 2)


def calculate_dependents_deductible(current_deductibles_model: object, employee: object):
    return round(employee.no_dependents * 0.7 * \
        current_deductibles_model.base_deductible, 2)


def calculate_disabled_dependents(current_deductibles_model: object, employee: object):
    return round(employee.no_dependents_disabled * 0.4 * \
        current_deductibles_model.base_deductible, 2)


def calculate_disabled_dependents_100(current_deductibles_model: object, employee: object):
    return round(employee.no_dependents_disabled_100 * 0.5 * \
        current_deductibles_model.base_deductible, 2)
