from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.calculation_data_app.models import ContributionRate, Contribution


class ContributionsModel(models.Model):

    contributions_model_id = models.AutoField(primary_key=True)
    model_mark = models.CharField(
        verbose_name=_('Model mark'),
        unique=True,
        max_length=10,
        help_text=_('Up to 10 characters long textual ID of this model')
    )
    contributions = models.ManyToManyField(ContributionRate, verbose_name=_('Contributions'))

    class Meta:
        verbose_name = _('Contributions model')
        verbose_name_plural = _('Contributions models')

        db_table = 'contributions_models'

    def __str__(self):
        return f"{self.model_mark}"

    @staticmethod
    def get_by_mark(_model_mark: str) -> 'ContributionsModel':
        return ContributionsModel.objects.get(model_mark=_model_mark)

    @property
    def get_out_of_pay(self) -> List['Contribution']:
        # return Contribution.objects.filter(contributions.contribution.out_of_pay=True)
        pass

    @property
    def get_ontop_of_pay(self) -> List['Contribution']:
        # return self.contributions.filter(self.contributions.out_of_pay=False)
        pass
