
from django.db import models


class TaxCalculation(models.Model):
    year = models.IntegerField(unique=True)
    revenue = models.FloatField()
    cost = models.FloatField()
    tax = models.FloatField()

    class Meta:
        verbose_name = "Tax calculation"
        verbose_name_plural = "Tax calculations"


    def __str__(self):
        return f"{self.year} - {self.tax}"
