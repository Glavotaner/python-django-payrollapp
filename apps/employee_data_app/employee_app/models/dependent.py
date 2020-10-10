from django.db import models
from .person import Person

class Dependent(Person):

    child = models.BooleanField(default=False, verbose_name='Child')

    # FOREIGN KEYS
    dependent_of = models.ForeignKey('Employee', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pid}"
