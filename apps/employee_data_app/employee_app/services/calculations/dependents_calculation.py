from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from apps.employee_data_app.employee_app.models import Employee, Dependent

from apps.calculation_data_app.services import deductibles_calculation as dc


def update_employee(employee: 'Employee'):
    deps: List['Dependent'] = dc.get_dependents(employee)

    employee.no_dependents = dc.get_adult_dependents(deps)
    employee.no_children = len(dc.get_children(deps))

    employee.no_dependents_disabled = dc.get_disabled_dependents(deps, employee)
    employee.no_dependents_disabled_100 = dc.get_disabled_dependents_100(deps, employee)

    employee.save(update_fields=[
        'no_dependents', 'no_children', 'no_dependents_disabled', 'no_dependents_disabled_100'
    ])
