from apps.employee_data_app.employee_app.models.dependent import Dependent


def calculate_no_children(pid: str) -> int:
    dep_counter = 0

    for dependent in Dependent.objects.filter(dependent_of=pid).all():
        if dependent.age <= 16:
            dep_counter += 1

    return dep_counter


def calculate_no_dependents(pid: str) -> int:
    dep_counter = 0

    for dependent in Dependent.objects.filter(dependent_of=pid).all():
        if dependent.child:
            dep_counter += 1

    return dep_counter


def caluclate_no_dependents_disabled(pid: str) -> int:
    dep_counter = 0

    for dependent in Dependent.objects.filter(dependent_of=pid).all():
        if dependent.disability == 'D':
            dep_counter += 1

    return dep_counter


def calculate_no_dependents_disabled_100(pid: str) -> int:
    dep_counter = 0

    for dependent in Dependent.objects.filter(dependent_of=pid).all():
        if dependent.disability == 'D100':
            dep_counter += 1

    return dep_counter
