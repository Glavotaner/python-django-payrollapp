from django.db import models
from django.utils.translation import gettext_lazy as _


class TaxBracket(models.Model):
    tax_bracket_id = models.AutoField(primary_key=True)

    amount_from = models.FloatField(verbose_name=_("Amount from"))
    amount_to = models.FloatField(verbose_name=_("Amount to"), null=True)

    tax_rate = models.FloatField(
        verbose_name=_("Tax rate"),
        help_text=_("Expressed as a decimal number")
    )

    class Meta:
        verbose_name = _('Tax model')
        verbose_name_plural = _('Tax models')

        db_table = 'tax_brackets'

    def __str__(self):
        return f"{self.tax_rate}"
