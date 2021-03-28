from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.calculation_data_app.models import ContributionPercentage


class ContributionsModel(models.Model):
    class Meta:
        verbose_name = _('Contributions model')
        verbose_name_plural = _('Contributions models')

    model_mark = models.CharField(
        verbose_name=_('Model mark'),
        unique=True,
        max_length=10,
        help_text=_('Up to 10 characters long textual ID of this model')
    )

    contributions = models.ManyToManyField(ContributionPercentage)

    def __str__(self):
        return f"{self.model_mark}"
