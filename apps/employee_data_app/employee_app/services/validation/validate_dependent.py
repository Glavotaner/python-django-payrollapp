from gettext import gettext as _

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from apps.employee_data_app.employee_app.models import Dependent


def validate_child_no_order(self):
    if not self.child and self.child_in_line:
        raise ValidationError(
            _('A dependent cannot have birth order data \
                    if they are not a child')
        )

    if self.child and not self.child_in_ine:
        raise ValidationError(
            _('A dependent cannot be labeled a child without birth order data')
        )


def validate_child_order(self):
    try:
        Dependent.objects.get(
            dependent_of=self.dependent_of, child_in_line=self.child_in_line
        )
    except ObjectDoesNotExist:
        return None

    raise ValidationError(
        _('Employee already has a child dependent\
            marked as their {order}. child'),
        params={'order': self.child_in_line}
    )
