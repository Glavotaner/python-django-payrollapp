from django.db import models
from apps.calculation_data_app.models import Contribution


class ContributionPercentage(models.Model):

    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    percentage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.contribution.name}: {str(self.percentage * 100)}%"
