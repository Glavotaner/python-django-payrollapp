from django.db import models


class ContractType(models.Model):

    contract_id = models.CharField(
        max_length=30, verbose_name='Contract ID', primary_key=True)
    contract_type = models.CharField(
        max_length=30, verbose_name='Contract type')

    def __str__(self):
        return self.contract_type
