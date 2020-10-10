from django.db import models


class Position(models.Model):

    position_name = models.CharField(
        max_length=30, verbose_name='Position name', unique=True)
    salary = models.FloatField(verbose_name='Salary')

    def __str__(self):
        return self.position_name
