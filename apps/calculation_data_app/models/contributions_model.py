from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import ContributionRate


class ContributionsModel(models.Model):
    contributions_model_id = models.AutoField(primary_key=True)
    model_mark = models.CharField(
        verbose_name=_('Model mark'),
        unique=True,
        max_length=10,
        help_text=_('Up to 10 characters long textual ID of this model')
    )
    contributions = models.ManyToManyField(
        ContributionRate, verbose_name=_('Contributions'))

    retired = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('Retired')
    )

    class Meta:
        app_label = 'calculation_data_app'
        verbose_name = _('Contributions model')
        verbose_name_plural = _('Contributions models')

        db_table = 'contributions_models'

    def __str__(self):
        return f"{self.model_mark}"

    @staticmethod
    def get_by_mark(_model_mark: str) -> 'ContributionsModel':
        return ContributionsModel.objects.get(model_mark=_model_mark)

    @staticmethod
    def get_current_contrib_models() -> List['ContributionsModel']:
        return ContributionsModel.objects.filter(retired=False)

    @property
    def get_contribs_from_pay(self) -> List['ContributionRate']:
        return self.contributions.filter(contribution__from_pay=True)

    @property
    def get_contribs_other(self) -> List['ContributionRate']:
        return self.contributions.filter(contribution__from_pay=False)
