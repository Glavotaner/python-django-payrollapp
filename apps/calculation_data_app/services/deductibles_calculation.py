from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.employee_data_app.employee_app.models import Employee, Dependent

from django.utils.timezone import datetime

from ..models import DeductiblesModel


def get_deductibles_model(accounting_date: datetime) -> DeductiblesModel:
    return DeductiblesModel.objects.filter(valid_from__lte=accounting_date).latest()


def get_dependents(employee: 'Employee') -> List:
    from apps.employee_data_app.employee_app.models import Dependent
    return Dependent.objects.filter(dependent_of=employee.pid)


def get_children(dependents: List['Dependent']) -> List:
    return [] if not dependents else [person for person in dependents if person.child_in_line]


def get_adult_dependents(dependents: List['Dependent']) -> int:
    return 0 if not dependents else len([person for person in dependents if not person.child_in_line])


def get_disabled_dependents(dependents: List['Dependent'], employee=None) -> int:
    if not dependents:
        return 0

    dependents: List['Dependent'] = [person for person in dependents if person.disability and person.disability == 'D']

    if not employee and len(dependents) > 0: employee = dependents[0].dependent_of

    return len(dependents) + 1 if employee.disability == 'D' else len(dependents)


def get_disabled_dependents_100(dependents: List['Dependent'], employee=None) -> int:
    if not dependents:
        return 0

    dependents = [person for person in dependents if person.disability and person.disability == 'D100']

    if not employee and len(dependents) > 0: employee = dependents[0].dependent_of

    return len(dependents) + 1 if employee.disability == 'D100' else len(dependents)


def get_children_coefs(deductibles_model: DeductiblesModel) -> dict:
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


def get_children_coef_gt9(child_rn: int, children_coefs: dict = None) -> float:
    if not children_coefs:
        children_coefs: dict = get_children_coefs(get_deductibles_model(datetime.today()))

    multiplication_coef: float = children_coefs.get('gt')

    if child_rn == 10:
        return multiplication_coef + children_coefs.get('9')
    else:
        return (multiplication_coef + children_coefs.get('9')) + ((child_rn - 10) * multiplication_coef)


class DeductibleCalculated:

    def __init__(self, deductibles_model: DeductiblesModel, employee):
        self.deductibles_model = deductibles_model
        self.employee = employee

    @property
    def personal_deductible(self):
        return round(self.deductibles_model.personal_deductible_coef * self.deductibles_model.base_deductible, 2)

    @property
    def children_deductible(self) -> float:

        deductible: float = 0

        children: List = get_children(get_dependents(self.employee))

        child_coefs: dict = get_children_coefs(self.deductibles_model)

        for child in children:
            if child.child_in_line < 10:
                deductible += child_coefs.get(str(child.child_in_line)) * self.deductibles_model.base_deductible
            else:
                deductible += get_children_coef_gt9(child.child_in_line, child_coefs) * \
                              self.deductibles_model.base_deductible

        return round(deductible, 2)

    @property
    def adults_deductible(self):
        return round(self.deductibles_model.base_deductible * (
                self.deductibles_model.dependent *
                get_adult_dependents(get_dependents(self.employee))
        ), 2)

    @property
    def disabled_deductible(self):
        return round(self.deductibles_model.base_deductible * (
                self.deductibles_model.disabled_dependent *
                get_disabled_dependents(get_dependents(self.employee))
        ), 2)

    @property
    def disabled_100_deductible(self):
        return round(self.deductibles_model.base_deductible * (
                self.deductibles_model.disabled_dependent_100 *
                get_disabled_dependents_100(get_dependents(self.employee))
        ), 2)

    @property
    def total_deductible(self):
        return round(self.children_deductible +
                     self.adults_deductible +
                     self.disabled_deductible +
                     self.disabled_100_deductible +
                     self.personal_deductible, 2)
