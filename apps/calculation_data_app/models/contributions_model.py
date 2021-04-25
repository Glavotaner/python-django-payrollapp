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
    contributions = models.ManyToManyField(ContributionRate, verbose_name=_('Contributions'))

    retired = models.BooleanField()

    class Meta:
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
        return ContributionsModel.objects.raw("""
        SELECT * FROM contribution_rates cr
        INNER JOIN contributions_models_contributions cmc on cr.contribution_rate_id = cmc.contributionrate_id
        INNER JOIN contributions c on c.contribution_id = cr.contribution_id
        WHERE cmc.contributionsmodel_id = %s AND c.from_pay = 1 
        """, params=[self.contributions_model_id])

    @property
    def get_contribs_other(self) -> List['ContributionRate']:
        return ContributionsModel.objects.raw("""
            SELECT * FROM contribution_rates cr
            INNER JOIN contributions_models_contributions cmc on cr.contribution_rate_id = cmc.contributionrate_id
            INNER JOIN contributions c on c.contribution_id = cr.contribution_id
            WHERE cmc.contributionsmodel_id = %s AND c.from_pay = 0 
            """, params=[self.contributions_model_id])
