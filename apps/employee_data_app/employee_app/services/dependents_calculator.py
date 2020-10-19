from apps.employee_data_app.employee_app.models.dependent import Dependent
from django.utils.translation import gettext_lazy as _


def _no_children(pid: str) -> int:

    deps = Dependent.objects.filter(dependent_of=pid).all()

    return sum(map(lambda d: d.child and d.disability == _('N'), deps))


def _no_dependents(pid: str) -> int:

    deps = Dependent.objects.filter(dependent_of=pid).all()

    return sum(map(lambda d: not d.child and d.disability == _('N'), deps))


def _no_dependents_disabled(pid: str) -> int:

    deps = Dependent.objects.filter(dependent_of=pid).all()

    return sum(map(lambda d: d.disability == _('D'), deps))


def _no_dependents_disabled_100(pid: str) -> int:

    deps = Dependent.objects.filter(dependent_of=pid).all()

    return sum(map(lambda d: d.disability == _('D100'), deps))
