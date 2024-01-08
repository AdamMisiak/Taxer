
from django.db import models


class TaxSummary(models.Model):
    year = models.IntegerField(unique=True)
    revenue = models.FloatField()
    cost = models.FloatField()
    tax = models.FloatField()

    class Meta:
        verbose_name = "Tax summary"
        verbose_name_plural = "Tax summary"


    def __str__(self):
        return f"{self.year} - {self.tax}"
