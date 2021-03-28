from gettext import gettext as _

from django.db import models


class WageParametersModel(models.Model):
    class Meta:
        verbose_name = 'Wage parameters model'
        verbose_name_plural = 'Wage parameters models'

    min_base = models.FloatField(
        verbose_name=_('Contributions minimal base'),
        help_text=_("The year's legal minimum contributions base. Use '.' as decimal point"),
        default=3321.96
    )

    max_base = models.FloatField(
        verbose_name=_('Contributions maximum base'),
        help_text=_("The year's legal maximum contributions base. Use '.' as decimal point"),
        default=55086
    )

    min_wage = models.FloatField(verbose_name=_('Minimum wage'))

    night_hours = models.FloatField(verbose_name=_('Night work multiplication coefficient'), default=2)
    sunday_hours = models.FloatField(verbose_name=_('Sunday work multiplication coefficient'), default=2)
    holiday_hours = models.FloatField(verbose_name=_('Holiday work multiplication coefficient'), default=2)
    overtime_hours = models.FloatField(verbose_name=_('Overtime work multiplication coefficient'), default=2)

    @property
    def work_type_coefs(self) -> dict:
        hours_coefs: dict = {}
        
        for field in self._meta.fields:
            if field.name.endswith('hours'):
                hours_coefs[field.name] = getattr(self, field.name)

        return hours_coefs
