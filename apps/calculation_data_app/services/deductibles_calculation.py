from apps.employee_data_app.employee_app.models import Employee, Dependent
from datetime import date
from typing import List

from ..models import DeductiblesModel


def get_children_coefs(deductibles_model: DeductiblesModel = None) -> dict:
    deductibles_model: DeductiblesModel = deductibles_model if deductibles_model else DeductiblesModel.get_valid_deductibles_model(
        date.today())

    return {
        '1': deductibles_model.first_child,
        '2': deductibles_model.second_child,
        '3': deductibles_model.third_child,
        '4': deductibles_model.fourth_child,
        '5': deductibles_model.fifth_child,
        '6': deductibles_model.sixth_child,
        '7': deductibles_model.seventh_child,
        '8': deductibles_model.eighth_child,
        '9': deductibles_model.ninth_child,
        'gt': deductibles_model.multiplication_coef
    }


def get_children_coef_gt9(
        child_rn: int, children_coefs: dict = None
) -> float:
    if not children_coefs:
        children_coefs: dict = get_children_coefs()

    multiplication_coef: float = children_coefs.get('gt')

    if child_rn == 10:
        return multiplication_coef + children_coefs.get('9')
    else:
        return (multiplication_coef + children_coefs.get('9')) + ((child_rn - 10) * multiplication_coef)


class DeductibleCalculated:

    def __init__(self,
                 deductibles_model: DeductiblesModel,
                 employee: Employee):
        self.deductibles_model: DeductiblesModel = deductibles_model
        self.employee: Employee = employee

    @property
    def personal_deductible(self):
        return round(self.deductibles_model.personal_deductible_coef * self.deductibles_model.base_deductible, 2)

    @property
    def children_deductible(self) -> float:

        deductible: float = 0

        children: List[Dependent] = self.employee.get_children_list

        child_coefs: dict = get_children_coefs(self.deductibles_model)

        for child in children:
            if child.child_in_line < 10:
                deductible += child_coefs.get(str(child.child_in_line)) * \
                    self.deductibles_model.base_deductible
            else:
                deductible += get_children_coef_gt9(child.child_in_line, child_coefs) * \
                    self.deductibles_model.base_deductible

        return round(deductible, 2)

    @property
    def adults_deductible(self):
        return round(self.deductibles_model.base_deductible * (
            self.deductibles_model.dependent *
            self.employee.get_adult_dependents_count
        ), 2)

    @property
    def disabled_deductible(self):
        return round(self.deductibles_model.base_deductible * (
            self.deductibles_model.disabled_dependent_i *
            self.employee.get_disabled_dependents_count
        ), 2)

    @property
    def disabled_100_deductible(self):
        return round(self.deductibles_model.base_deductible * (
            self.deductibles_model.disabled_dependent_i100 *
            self.employee.get_disabled_dependents_100_count
        ), 2)

    @property
    def total_deductible(self):
        return round(self.children_deductible +
                     self.adults_deductible +
                     self.disabled_deductible +
                     self.disabled_100_deductible +
                     self.personal_deductible, 2)
