from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.employee_data_app.employee_app.models import Employee


def update_employee(employee: 'Employee') -> None:
    employee.no_dependents = employee.get_adult_dependents_count
    employee.no_children = len(employee.get_children_list)

    employee.no_dependents_disabled = employee.get_disabled_dependents_count
    employee.no_dependents_disabled_100 = employee.get_disabled_dependents_100_count

    employee.save(update_fields=[
        'no_dependents', 'no_children', 'no_dependents_disabled', 'no_dependents_disabled_100'
    ])
