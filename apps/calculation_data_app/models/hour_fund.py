from django.db import models
from django.utils.translation import gettext_lazy as _


class HourFund(models.Model):
    hour_fund_id = models.AutoField(primary_key=True)

    year = models.IntegerField(verbose_name=_('Year'), default=2020)
    month = models.IntegerField(verbose_name=_('Month'))
    total_hours = models.IntegerField(verbose_name=_('Total hours'))

    class Meta:
        verbose_name = _('Hour fund')
        verbose_name_plural = _('Hour funds')

        db_table = 'hour_funds'

    def __str__(self):
        return f"{self.period_id}"

    @staticmethod
    def get_hour_fund_for_period(year: int, month: int) -> int:
        return HourFund.objects.get(year=year, month=month).total_hours

    @property
    def period_id(self):
        return str(self.year) + ('0' + str(self.month))[1:]
