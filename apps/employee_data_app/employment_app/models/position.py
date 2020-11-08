from django.db import models
from django.utils.translation import gettext_lazy as _

class Position(models.Model):
    
    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
        

    position_name = models.CharField(
        max_length=80, verbose_name = _('Position name'), unique=True)
    salary = models.FloatField(verbose_name = _('Salary'), default = 5600)


    def __str__(self):
        return self.position_name
