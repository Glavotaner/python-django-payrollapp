
def _personal_deductible_amount(self):
    return round(self.current_deductibles_model.base_deductible * \
        self.current_deductibles_model.personal_deductible_coef, 2)


def _deductible_children(self):
    child_coefs = [0.7, 1.0, 1.4, 1.9, 2.5, 3.2, 4.0, 4.9, 5.9, 7]

    if 0 < self.employee.no_children < 10:
        return round(child_coefs[self.employee.no_children - 1] * \
            self.current_deductibles_model.base_deductible, 2)
    elif self.employee.no_children <= 0:
        return 0
    else:
        return round(((self.employee.no_children - 9) * 1.1 + 7) * \
            self.current_deductibles_model.base_deductible, 2)


def _deductible_dependents(self):
    return round(self.employee.no_dependents * 0.7 * \
        self.current_deductibles_model.base_deductible, 2)


def _deductible_dependents_disabled(self):
    return round(self.employee.no_dependents_disabled * 0.4 * \
        self.current_deductibles_model.base_deductible, 2)


def _deductible_dependents_disabled_100(self):
    return round(self.employee.no_dependents_disabled_100 * 0.5 * \
        self.current_deductibles_model.base_deductible, 2)

def _total_deductibles(self):
    return round(self.personal_deductible_amount + self.deductible_children + self.deductible_dependents + self.deductible_dependents_disabled + self.deductible_dependents_disabled_100, 2)
